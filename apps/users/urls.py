from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users import viewsets
from apps.users.views import views
from apps.users.views import form_views

router = DefaultRouter()
router.register(r'users', viewsets.UserViewSet)

app_name = 'users'

urlpatterns = [
    # user
    path('api/', include(router.urls)),
    path('api/register/', views.CreateUser.as_view(), name='register'),
    path('user/signup/', form_views.CustomUserSignUp.as_view(), name='user_sign_up'),
    path('user/login/', form_views.CustomUserSignIn.as_view(), name='user_sign_in'),
    path('user/signout/', form_views.SignOutView.as_view(), name='user_sign_out'),
    path('user/<pk>/edit', form_views.CustomUserEdit.as_view(), name='user_edit'),
    path('user/<pk>/password', form_views.CustomUserPassword.as_view(), name='user_password'),
    path('user/<pk>/todoschoices', form_views.CustomUserToDosChoices.as_view(), name='user_to_dos_choices'),
    path('user/<pk>/pagechoice', form_views.CustomUserPageChoice.as_view(), name='user_page_choice'),
    path('user/<pk>/goalviewchoice', form_views.CustomUserGoalViewChoices.as_view(), name='user_goal_view_choices'),
    path('user/<pk>/treeviewchoices', form_views.CustomUserTreeViewChoices.as_view(), name='user_treeview_choices'),
    path('user/<pk>/strategy-main-choices/', form_views.UpdateStrategyMainChoicesUser.as_view(),
         name='update_strategy_main_choice_user'),
    # views
    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('settings/', views.SettingsView.as_view(), name='settings_view')
]
