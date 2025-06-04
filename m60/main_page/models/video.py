from .base import BaseModel
from django.db import models
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

class Video(BaseModel):
    SERVICE_CHOICES = [
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    url = models.URLField("Ссылка на видео", max_length=500)
    service = models.CharField("Сервис", max_length=20, choices=SERVICE_CHOICES, blank=True)
    title = models.CharField("Название", max_length=255, blank=True)
    author = models.CharField("Автор", max_length=100, blank=True)
    duration = models.PositiveIntegerField("Длительность (сек)", blank=True, null=True)
    thumbnail_url = models.URLField("Превью", max_length=500, blank=True)

    def save(self, *args, **kwargs):
        """Автоматически определяет сервис и заполняет метаданные"""
        self.detect_service()
        self.extract_metadata()
        super().save(*args, **kwargs)

    def detect_service(self):
        """Определяет видеохостинг по URL"""
        if "youtube.com" in self.url or "youtu.be" in self.url:
            self.service = "youtube"
        else:
            self.service = "other"

    def extract_metadata(self):
        """Заполняет данные в зависимости от сервиса"""
        if self.service == "youtube":
            self.fetch_youtube_data()

    def fetch_youtube_data(self):
        """Получает данные для YouTube через API"""
        video_id = self.extract_youtube_id()
        if not video_id:
            raise ValueError("Невозможно извлечь ID видео")
        
        api_key = os.getenv("YOUTUBE_API_KEY")
        base_url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,contentDetails",
            "id": video_id,
            "key": api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Ошибка при получении данных: {data['error']['message']}")

        items = data.get('items')
        if not items:
            raise Exception("Видео не найдено")

        snippet = items[0]['snippet']
        content_details = items[0]['contentDetails']

        self.title = snippet.get('title', '')
        self.author = snippet.get('channelTitle', '')
        self.thumbnail_url = snippet.get('thumbnails', {}).get('high', {}).get('url', '')
        self.duration = self.parse_duration(content_details.get('duration'))

    def parse_duration(self, duration_str):
        """ Преобразует длительность формата ISO8601 (PT#H#M#S) в секунды """
        regex = r'PT(\d+H)?(\d+M)?(\d+S)'
        matches = re.match(regex, duration_str)
        hours = int(matches.group(1)[:-1]) if matches.group(1) else 0
        minutes = int(matches.group(2)[:-1]) if matches.group(2) else 0
        seconds = int(matches.group(3)[:-1]) if matches.group(3) else 0
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds


    def extract_youtube_id(self):
        """Извлекает ID видео из YouTube-ссылки"""
        patterns = [
            r"(?:youtube\.com/watch\?v=|youtu\.be/)([^&?/]+)",
            r"(?:embed/|v/|shorts/)([^&?/]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return None
    
    def __str__(self):
        return f"{self.author}: {self.title}"