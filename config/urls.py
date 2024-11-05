from django.conf.urls.static import static
from apps.achievements.urls import router as achievements_router
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from apps.todos.urls import router as todos_router
from apps.users.urls import router as users_router
from apps.notes.urls import router as notes_router
from apps.goals.urls import router as goals_router
from apps.story.urls import router as story_router
from django.contrib import admin
from .filebrowser import site
from django.conf import settings
from django.urls import path
from rest_framework.authtoken import views

router = DefaultRouter()
router.registry.extend(todos_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(notes_router.registry)
router.registry.extend(goals_router.registry)
router.registry.extend(story_router.registry)
router.registry.extend(achievements_router.registry)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path("form/", include("apps.todos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
