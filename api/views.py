from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.pagination_classes import CustomPageNumberPagination
from api.permissions import ReadOnlyOrStaffUserPermission
from api.serializers import (
    CompletedLessonSerializer,
    CourseEnrollSerializer,
    CourseSerializer,
    StudentProgressSerializer,
)
from core.models import Course, Student


class CourseViewSet(ModelViewSet):
    permission_classes = (ReadOnlyOrStaffUserPermission,)
    queryset = Course.objects.prefetch_related("lessons").order_by("title")
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["user"] = self.request.user
        return ctx


class CourseEnrollView(CreateAPIView):
    permission_classes = (ReadOnlyOrStaffUserPermission,)
    serializer_class = CourseEnrollSerializer
    queryset = Course.students.through.objects.all()

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


class CompletedLessonView(CreateAPIView):
    serializer_class = CompletedLessonSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["student_id"] = self.request.user.id
        return ctx


class StudentsProgress(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentProgressSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all().prefetch_related(
                "courses", "completed_lessons"
            )
        return Student.objects.filter(id=self.request.user.id).prefetch_related(
            "courses", "completed_lessons"
        )
