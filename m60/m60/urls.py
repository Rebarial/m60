from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main_page.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + doc_urls
