from django.contrib.auth.models import User
from django.db import models

from core.managers import StaffManager, StudentsManager


class Student(User):

    class Meta:
        proxy = True

    objects = StudentsManager()


class StaffMember(User):

    class Meta:
        proxy = True

    objects = StaffManager()

    def save(self, *args, **kwargs):
        self.is_staff = True
        return super().save(*args, **kwargs)


class Course(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name="courses")
    created_by = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    students = models.ManyToManyField(Student, related_name="completed_lessons")
    duration = models.PositiveIntegerField(default=1, help_text="duration in minutes")

    def __str__(self):
        return self.title


from .signals import *
