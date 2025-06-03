from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ReviewsVideo

def get_video_data(request, video_id):
    try:
        video = get_object_or_404(ReviewsVideo, pk=video_id)
        
        response_data = {
            'status': 'success',
            'video': video.video_url,
        }
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=404)