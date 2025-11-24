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
# Зчитуємо ЗНАЧЕННЯ змінної середовища з НАЗВОЮ "BOT_TOKEN"
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
# Порт, який надає Render
PORT = int(os.environ.get("PORT", 8080))
# URL, який надає Render
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
    text = update.message.text
    if "MagSafe" in text or "хочу" in text:
        await update.message.reply_text("Чудовий вибір! MagSafe — це автоматичне вирівнювання та швидка зарядка. Переходжу до каталогу...")
    else:
        await update.message.reply_text("Зрозуміло. Здається, у мене немає відповіді на це. Передаю Ваше питання менеджеру!")


# --- ГОЛОВНА ФУНКЦІЯ ЗАПУСКУ ---

def main() -> None:
    """Запускає бота у режимі WebHook."""
    
    # ПЕРЕВІРКА, яка раніше давала помилку, тепер має спрацювати успішно!
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.error("КРИТИЧНА ПОМИЛКА: BOT_TOKEN або WEBHOOK_URL не визначені. Перевірте змінні середовища Render.")
        return

    # 1. Створення Application
    application = Application.builder().token(BOT_TOKEN).updater(None).build()

    # 2. Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 3. Запуск у режимі WebHook
    logger.info(f"Запуск бота на WebHook URL: {WEBHOOK_URL} з портом: {PORT}")

    application.run_webhook(
        listen="0.0.0.0", 
        port=PORT,         
        url_path=BOT_TOKEN, 
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )


if __name__ == '__main__':
    main()
