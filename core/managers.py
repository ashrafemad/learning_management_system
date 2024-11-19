from django.contrib.auth.models import UserManager


class StudentsManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class StaffManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
