from django.urls import path
from .views import views
from .views import form_views


app_name = 'users'
urlpatterns = [
    # user
    path('user/signup/', form_views.CustomUserSignUp.as_view(), name='user_sign_up'),
    path('user/login/', form_views.CustomUserSignIn.as_view(), name='user_sign_in'),
    path('user/signout/', form_views.SignOutView.as_view(), name='user_sign_out'),
    path('user/<pk>/edit', form_views.CustomUserEdit.as_view(), name='user_edit'),
    path('user/<pk>/password', form_views.CustomUserPassword.as_view(), name='user_password'),
    path('user/<pk>/starchoicesheader', form_views.CustomUserStarChoicesHeader.as_view(), name='user_star_choices_header'),
    path('user/<pk>/starchoices', form_views.CustomUserStarChoices.as_view(), name='user_star_choices'),
    path('user/<pk>/todoschoices', form_views.CustomUserToDosChoices.as_view(), name='user_to_dos_choices'),
    path('user/<pk>/pagechoice', form_views.CustomUserPageChoice.as_view(), name='user_page_choice'),
    # views
    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('settings/', views.SettingsView.as_view(), name='settings_view')
]
