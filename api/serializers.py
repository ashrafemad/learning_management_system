from collections import defaultdict

from django.db.models import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Course, Lesson, StaffMember, Student


class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = ("id", "username")


class LessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    course = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = ("id", "title", "course", "duration")


class CourseSerializer(serializers.ModelSerializer):
    created_by = StaffMemberSerializer(read_only=True, many=False)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ("id", "title", "lessons", "created_by")

    def create(self, validated_data):
        lessons = validated_data.pop("lessons", [])
        validated_data["created_by"] = self.context["user"]
        course = super().create(validated_data)
        to_create_lessons = []
        for lesson in lessons:
            to_create_lessons.append(Lesson(title=lesson["title"], course=course))
        Lesson.objects.bulk_create(to_create_lessons)
        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons", [])
        course = super().update(instance, validated_data)
        related_lessons = course.lessons.all()

        # Map each id to a lesson object to reduce later loop queries
        course_lessons = {l.id: l for l in related_lessons}
        to_create_lessons = []
        to_update_lessons = []
        for lesson in lessons:
            if lesson.get("id") and lesson["id"] in course_lessons:
                course_lessons[lesson["id"]].title = lesson["title"]
                to_update_lessons.append(course_lessons[lesson["id"]])
            else:
                to_create_lessons.append(Lesson(title=lesson["title"], course=course))
        created_objs = Lesson.objects.bulk_create(to_create_lessons)
        Lesson.objects.bulk_update(to_update_lessons, fields=["title"])

        # Collect lesson objects to stay with the course
        all_objects = created_objs + to_update_lessons

        # Collect lesson objects to be deleted that exists now in related_lessons and not in passed objects
        to_delete_ids = [les.id for les in related_lessons if les not in all_objects]
        if to_delete_ids:
            related_lessons.filter(id__in=to_delete_ids).delete()

        # Set created/updated objects to the many to many relation
        course.lessons.set(all_objects)
        return course


class CourseEnrollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course.students.through
        fields = ("student", "course")


class CompletedLessonSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)

    class Meta:
        model = Lesson.students.through
        fields = ("lesson", "lesson_title")

    def validate_lesson(self, lesson_id):
        student_id = self.context["student_id"]
        if Lesson.students.through.objects.filter(
            student_id=student_id, lesson_id=lesson_id
        ).exists():
            raise ValidationError(
                {"error": f"Lesson {lesson_id} already marked as completed!"}
            )
        return lesson_id

    def create(self, validated_data):
        validated_data["student_id"] = self.context["student_id"]
        return super().create(validated_data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student_courses_ids = Course.students.through.objects.filter(
            student_id=self.context["student_id"]
        ).values_list("course_id", flat=True)
        self.fields["lesson"].queryset = Lesson.objects.filter(
            course_id__in=student_courses_ids
        )


class StudentProgressSerializer(serializers.ModelSerializer):

    courses_progress = serializers.SerializerMethodField()

    def get_courses_progress(self, obj):
        student_courses = (
            obj.courses.all()
            .prefetch_related("lessons")
            .annotate(lessons_count=Count("lessons"))
        )
        student_completed_lessons_ids = dict(
            obj.completed_lessons.values_list("id", "title")
        )
        courses_data = defaultdict(dict)
        for course in student_courses:
            all_lessons = course.lessons.all()
            courses_data[course.title]["total_lessons_count"] = course.lessons_count
            courses_data[course.title]["completed_lessons"] = [
                l.title for l in all_lessons if l.id in student_completed_lessons_ids
            ]
        return courses_data

    class Meta:
        model = Student
        fields = ("username", "courses_progress")
