# Generated by Django 5.2.1 on 2025-06-04 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(unique=True, verbose_name='ID чата')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('subscribed_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')),
            ],
            options={
                'verbose_name': 'Подписчик Telegram',
                'verbose_name_plural': 'Подписчики Telegram',
            },
        ),
    ]
