import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Налаштування логування (дуже важливо для Render)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ЗМІННІ СЕРЕДОВИЩА ---
# Токен бота
BOT_TOKEN = os.environ.get("8270132256:AAELg2DTV0qifcHN4q8uvqrEFy6O75yMPcc")
# Порт, який надає Render
PORT = int(os.environ.get("PORT", 8080))
# URL, який надає Render (наприклад: https://your-service-name.onrender.com/)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") 


# --- ФУНКЦІЇ-ОБРОБНИКИ (ПРИКЛАД) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє команду /start та відповідає привітанням."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привіт, {user.mention_html()}! Я ваш консультант із Smart Accessories. Готовий допомогти з MagSafe!",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє команду /help."""
    await update.message.reply_text("Я тут, щоб допомогти Вам вибрати ідеальні аксесуари Apple. Напишіть свій запит!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробляє текстові повідомлення."""
    # Тут має бути логіка Вашого ланцюжка Telegram-бота!
    # Наприклад, відповідь на запит "хочу MagSafe"
    text = update.message.text
    if "MagSafe" in text or "хочу" in text:
        await update.message.reply_text("Чудовий вибір! MagSafe — це автоматичне вирівнювання та швидка зарядка. Переходжу до каталогу...")
    else:
        await update.message.reply_text("Зрозуміло. Здається, у мене немає відповіді на це. Передаю Ваше питання менеджеру!")


# --- ГОЛОВНА ФУНКЦІЯ ЗАПУСКУ ---

def main() -> None:
    """Запускає бота у режимі WebHook."""
    
    if not BOT_TOKEN or not WEBHOOK_URL:
        # Ця перевірка спричиняла помилку "BOT_TOKEN або WEBHOOK_URL не визначені."
        # Ви маєте виправити змінні середовища на Render!
        logger.error("КРИТИЧНА ПОМИЛКА: BOT_TOKEN або WEBHOOK_URL не визначені. Перевірте змінні середовища Render.")
        return

    # 1. Створення Application
    application = Application.builder().token(BOT_TOKEN).build()

    # 2. Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 3. Запуск у режимі WebHook
    # Render вимагає саме таку конфігурацію: слухати 0.0.0.0 на наданому PORT
    logger.info(f"Запуск бота на WebHook URL: {WEBHOOK_URL} з портом: {PORT}")

    application.run_webhook(
        listen="0.0.0.0", 
        port=PORT,         
        url_path=BOT_TOKEN, # Використовуємо токен як шлях для безпеки
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )


if __name__ == '__main__':
    # Фіксуємо IndentationError: переконайтеся, що всі відступи в файлі коректні!
    main()
