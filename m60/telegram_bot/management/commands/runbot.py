from django.core.management.base import BaseCommand
from telegram_bot.telegram_bot_functions import setup_bot

class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write("Starting Telegram bot...")
        setup_bot()