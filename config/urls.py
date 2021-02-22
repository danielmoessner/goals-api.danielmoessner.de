from django.conf.urls.static import static
from django.shortcuts import redirect
from django.conf.urls import include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from .filebrowser import site
from config.auth import obtain_auth_token
from django.conf import settings
from django.urls import path
from apps.todos.urls import router as todos_router

router = DefaultRouter()
router.registry.extend(todos_router.registry)

urlpatterns = [
    path('', include(router.urls)),
    path('g/', include('apps.goals.urls')),
    path('u/', include('apps.users.urls')),
    path('n/', include('apps.notes.urls')),
    path('filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
