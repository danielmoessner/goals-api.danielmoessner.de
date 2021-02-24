from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import viewsets
from apps.users import views

router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('api/register/', views.CreateUser.as_view(), name='register'),
#     path('api/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
# ]
