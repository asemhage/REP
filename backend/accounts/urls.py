from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginView, MeView, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("users/me/", MeView.as_view(), name="user-me"),
    path("", include(router.urls)),
]

