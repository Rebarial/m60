from django.db import models
from main_page.models.base import BaseModel

class TelegramSubscriber(BaseModel):
    chat_id = models.BigIntegerField(unique=True, verbose_name="ID чата")
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписчик Telegram"
        verbose_name_plural = "Подписчики Telegram"

    def __str__(self):
        return f"{self.username or self.first_name} ({self.chat_id})"