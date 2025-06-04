from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Video

@api_view(['GET'])
def get_video_url(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
        return Response({'url': video.url}, status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)