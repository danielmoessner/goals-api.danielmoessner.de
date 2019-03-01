from django.urls import path
from . import views


app_name = "core"
urlpatterns = [
    # PAGE
    path('', views.IndexView.as_view(), name='index'),
    path('redirect/', views.RedirectView.as_view(), name='redirect')
]
