import os
import logging
from telegram import Update, Bot # <-- Додаємо імпорт Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    Updater 
)

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ЗМІННІ СЕРЕДОВИЩА ---
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
PORT = int(os.environ.get("PORT", 8080))
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
    text = update.message.text
    if text and ("MagSafe" in text or "хочу" in text):
        await update.message.reply_text("Чудовий вибір! MagSafe — це автоматичне вирівнювання та швидка зарядка. Переходжу до каталогу...")
    else:
        await update.message.reply_text("Зрозуміло. Здається, у мене немає відповіді на це. Передаю Ваше питання менеджеру!")


# --- ГОЛОВНА ФУНКЦІЯ ЗАПУСКУ ---

def main() -> None:
    """Запускає бота у режимі WebHook на Render."""
    
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.error("КРИТИЧНА ПОМИЛКА: BOT_TOKEN або WEBHOOK_URL не визначені. Перевірте змінні середовища Render.")
        return

    # 1. Створення об'єкта Bot та передача токена
    bot_obj = Bot(BOT_TOKEN)

    # 2. Створення Application З ВИКОРИСТАННЯМ Updater, але БЕЗ токена в ланцюжку
    # Це обходить внутрішній конфлікт і вирішує RuntimeError.
    application = (
        Application.builder()
        .bot(bot_obj) # <-- Передаємо об'єкт Bot
        .updater(Updater) # <-- Встановлюємо Updater
        .build()
    )

    # 3. Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 4. Запуск у режимі WebHook
    logger.info(f"Запуск бота на WebHook URL: {WEBHOOK_URL} з портом: {PORT}")

    application.run_webhook(
        listen="0.0.0.0", 
        port=PORT,         
        url_path=BOT_TOKEN, 
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )


if __name__ == '__main__':
    main()
