from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from apps.todos.urls import router as todos_router
from apps.users.urls import router as users_router
from django.contrib import admin
from .filebrowser import site
from django.conf import settings
from django.urls import path

router = DefaultRouter()
router.registry.extend(todos_router.registry)
router.registry.extend(users_router.registry)

urlpatterns = [
    path('', include(router.urls)),
    path('g/', include('apps.goals.urls')),
    path('n/', include('apps.notes.urls')),
    path('filebrowser/', site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
