from django.urls import path
from apps.notes.views import views
from apps.notes.views import form_views


app_name = 'notes'
urlpatterns = [
    # note
    path('note/add/', form_views.NoteAdd.as_view(), name='note_add'),
    path('note/<pk>/edit', form_views.NoteEdit.as_view(), name='note_edit'),
    path('note/<pk>/delete', form_views.NoteDelete.as_view(), name='note_delete'),
    # views
    path('', views.DashboardView.as_view(), name='index'),
    path('note/<pk>/', views.NoteView.as_view(), name='note'),
]

