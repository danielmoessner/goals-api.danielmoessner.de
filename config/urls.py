from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .filebrowser import site
from apps.achievements.urls import router as achievements_router
from apps.goals.urls import router as goals_router
from apps.notes.urls import router as notes_router
from apps.story.urls import router as story_router
from apps.todos.urls import router as todos_router
from apps.users.urls import router as users_router
from config.form import form_view, global_form_view

router = DefaultRouter()
router.registry.extend(todos_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(notes_router.registry)
router.registry.extend(goals_router.registry)
router.registry.extend(story_router.registry)
router.registry.extend(achievements_router.registry)

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("filebrowser/", site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
    path("todos/", include("apps.todos.urls")),
    path("achievements/", include("apps.achievements.urls")),
    path("notes/", include("apps.notes.urls")),
    path("story/", include("apps.story.urls")),
    path("users/", include("apps.users.urls")),
    path("goals/", include("apps.goals.urls")),
    path("form/<str:form_name>/", form_view, name="form"),
    path("global-form/<str:form_name>/", global_form_view, name="global_form"),
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
