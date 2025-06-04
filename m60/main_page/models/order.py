from django.db import models
from .base import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram_bot.telegram_bot_functions import send_order_notification_task

class Order(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Имя")
    telephone = models.CharField(max_length=12, verbose_name="Телефон")

    class Meta:
        verbose_name = "Заявка на обучение"
        verbose_name_plural = "Заявка на обучение"


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
        send_order_notification_task.delay(instance.id)