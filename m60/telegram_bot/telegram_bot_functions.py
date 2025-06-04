from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram_bot.models.telegram import TelegramSubscriber
from asgiref.sync import sync_to_async, async_to_sync
from celery import shared_task
import os
import asyncio
from telegram_bot.models import TelegramSubscriber
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)

MENU_KEYBOARD = ReplyKeyboardMarkup(
    [["Подписаться на уведомления", "Отписаться от уведомлений"]],
    resize_keyboard=True
)

@sync_to_async
def get_or_create_subscriber(chat_id, username, first_name):
    return TelegramSubscriber.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'username': username,
            'first_name': first_name,
        }
    )

@sync_to_async
def delete_subscriber(chat_id):
    return TelegramSubscriber.objects.filter(chat_id=chat_id).delete()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, "Добро пожаловать! Выберите действие:")

async def show_menu(update: Update, text: str):
    await update.message.reply_text(
        text,
        reply_markup=MENU_KEYBOARD
    )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    
    subscriber, created = await get_or_create_subscriber(
        chat_id=chat_id,
        username=user.username,
        first_name=user.first_name
    )
    
    if created:
        await show_menu(update, "✅ Вы успешно подписались на уведомления!")
    else:
        await show_menu(update, "ℹ️ Вы уже подписаны на уведомления")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    deleted_count, _ = await delete_subscriber(chat_id)
    
    if deleted_count > 0:
        await show_menu(update, "❌ Вы отписались от уведомлений")
    else:
        await show_menu(update, "ℹ️ Вы не были подписаны на уведомления")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "Подписаться на уведомления":
        await subscribe(update, context)
    elif text == "Отписаться от уведомлений":
        await unsubscribe(update, context)
    else:
        await show_menu(update, "Пожалуйста, выберите действие из меню:")

@shared_task
def send_order_notification_task(order_id):
    """Синхронная Celery-задача для отправки уведомлений"""
    from main_page.models import Order
    try:
        order = Order.objects.get(id=order_id)
        subscribers = list(TelegramSubscriber.objects.all())
        
        if not subscribers:
            return
        
        message = (
            f"📌 Новая заявка на обучение!\n\n"
            f"👤 Имя: {order.name}\n"
            f"📞 Телефон: {order.telephone}\n"
        )
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        async def _send_messages():
            try:
                for subscriber in subscribers:
                    try:
                        await bot.send_message(
                            chat_id=subscriber.chat_id,
                            text=message
                        )
                        print(f"Сообщение отправлено {subscriber.chat_id}")
                    except Exception as e:
                        print(f"Ошибка при отправке {subscriber.chat_id}: {e}")
            except Exception as e:
                print(f"Критическая ошибка при отправке: {e}")
                raise
        
        if loop.is_running():
            asyncio.create_task(_send_messages())
        else:
            loop.run_until_complete(_send_messages())
            
    except Exception as e:
        print(f"Ошибка в задаче отправки уведомлений: {e}")
        raise


async def send_telegram_messages(subscribers, message):
    """Асинхронная функция для отправки сообщений"""
    for subscriber in subscribers:
        try:
            await bot.send_message(chat_id=subscriber.chat_id, text=message)
            print(f"Сообщение отправлено {subscriber.chat_id}")
        except Exception as e:
            print(f"Ошибка при отправке {subscriber.chat_id}: {e}")


def setup_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()