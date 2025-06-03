from django.contrib import admin
from django.urls import path
from main_page.views import get_video_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video/<int:video_id>/', get_video_data, name='get_video_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
