from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.models import StaffMember, Student


@admin.register(Student, StaffMember)
class UserAdmin(DjangoUserAdmin):
    pass
