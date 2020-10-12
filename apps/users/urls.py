from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import viewsets
from apps.users import views

router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)

app_name = 'users'

urlpatterns = [
    # user
    path('api/', include(router.urls)),
    path('api/register/', views.CreateUser.as_view(), name='register'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('user/login/', views.CustomUserSignIn.as_view(), name='user_sign_in'),
    path('user/signout/', views.SignOutView.as_view(), name='user_sign_out'),
    # views
    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('settings/', views.SettingsView.as_view(), name='settings_view')
]
