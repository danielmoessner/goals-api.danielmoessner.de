from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users import viewsets

from . import views

router = DefaultRouter()
router.register(r"users", viewsets.UserViewSet)


urlpatterns = [
    # auth stuff
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # register
    path("register/", views.CustomRegisterView.as_view(), name="register_user"),
    path(
        "register/success/",
        views.CustomRegisterDoneView.as_view(),
        name="register_user_done",
    ),
    path(
        "register/email-confirm/<uidb64>/<token>/",
        views.CustomRegisterConfirmEmailView.as_view(),
        name="register_confirm_email",
    ),
    # email change
    path("email-change/", views.ChangeEmailView.as_view(), name="change_email"),
    path(
        "email-change/abgesendet/",
        views.ChangeEmailDoneView.as_view(),
        name="change_email_done",
    ),
    path(
        "email-change/confirm/<uidb64>/<token>/",
        views.ChangeEmailConfirmView.as_view(),
        name="change_email_confirm",
    ),
    # password change
    path(
        "password-change/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "password-change/success/",
        views.ChangePasswordDoneView.as_view(),
        name="change_password_done",
    ),
    # password forgotten
    path(
        "password-forgotten/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-forgotten/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-forgotten/reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-forgotten/success/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
