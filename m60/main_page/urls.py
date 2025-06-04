from django.urls import path
from .views import get_video_url

urlpatterns = [
    path('video/<int:video_id>/', get_video_url, name='get_video_url'),
]