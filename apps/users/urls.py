from django.urls import path

from . import views

urlpatterns = [
    path("logout/", views.LogoutView.as_view(), name="logout"),
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
    path(
        "email-change/sent/",
        views.ChangeEmailDoneView.as_view(),
        name="change_email_done",
    ),
    path(
        "email-change/confirm/<uidb64>/<token>/",
        views.ChangeEmailConfirmView.as_view(),
        name="change_email_confirm",
    ),
    path(
        "password-change/success/",
        views.ChangePasswordDoneView.as_view(),
        name="change_password_done",
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
