import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- ЗМІННІ СЕРЕДОВИЩА ---
# Змінні читаються як і раніше
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") 


# --- ФУНКЦІЇ-ОБРОБНИКИ (v13 використовує sync-функції) ---

def start(update, context):
    """Обробляє команду /start."""
    user = update.effective_user
    update.message.reply_html(
        f"Привіт, {user.mention_html()}! Я ваш консультант із Smart Accessories. Готовий допомогти з MagSafe!",
    )

def help_command(update, context):
    """Обробляє команду /help."""
    update.message.reply_text("Я тут, щоб допомогти Вам вибрати ідеальні аксесуари Apple. Напишіть свій запит!")

def handle_message(update, context):
    """Обробляє текстові повідомлення."""
    text = update.message.text
    if text and ("MagSafe" in text or "хочу" in text):
        update.message.reply_text("Чудовий вибір! MagSafe — це автоматичне вирівнювання та швидка зарядка. Переходжу до каталогу...")
    else:
        update.message.reply_text("Зрозуміло. Здається, у мене немає відповіді на це. Передаю Ваше питання менеджеру!")


# --- ГОЛОВНА ФУНКЦІЯ ЗАПУСКУ ---

def main():
    """Запускає бота у режимі WebHook на Render (v13)."""
    
    if not BOT_TOKEN or not WEBHOOK_URL:
        logger.error("КРИТИЧНА ПОМИЛКА: BOT_TOKEN або WEBHOOK_URL не визначені. Перевірте змінні середовища Render.")
        return

    # 1. Створення Updater
    # (v13 використовує токен тут і не має конфлікту)
    updater = Updater(BOT_TOKEN)

    # 2. Отримання Dispatcher для реєстрації обробників
    dp = updater.dispatcher

    # 3. Реєстрація обробників
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # 4. Запуск у режимі WebHook
    logger.info(f"Запуск бота на WebHook URL: {WEBHOOK_URL} з портом: {PORT}")

    updater.start_webhook(
        listen="0.0.0.0", 
        port=PORT,         
        url_path=BOT_TOKEN, 
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
    # v13 не потребує додаткового методу stop/run_forever, він чекає HTTP-запитів.


if __name__ == '__main__':
    main()
