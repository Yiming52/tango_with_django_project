from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rango.urls')),
]


if settings.DEBUG:
    # Static files are automatically served in development by django.contrib.staticfiles.
    # Uncomment the following line if you need to explicitly serve static files.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Serve media files during development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
