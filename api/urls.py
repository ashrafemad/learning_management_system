from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import (
    CompletedLessonView,
    CourseEnrollView,
    CourseViewSet,
    StudentsProgress,
)

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API Docs",
        default_version="v1",
    ),
    public=settings.DEBUG,
)


router = routers.SimpleRouter()
router.register(r"courses", CourseViewSet)
urlpatterns = router.urls
urlpatterns += (
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("enroll-students/", CourseEnrollView.as_view(), name="enroll-students"),
    path("complete-lesson/", CompletedLessonView.as_view(), name="complete-lesson"),
    path("students-progress/", StudentsProgress.as_view(), name="students-progress"),
)
