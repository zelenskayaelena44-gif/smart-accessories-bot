import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Переменные (токен можно вставить прямо сюда для простоты) ---
# Для максимальной простоты вставьте токен прямо здесь:
BOT_TOKEN = "8270132256:AAELg2DTV0qifcHN4q8uvqrEFy6O75yMPcc" # <-- Замените на Ваш токен в кавычках!

# --- Функции-обработчики ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start и запускает приветствие."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я ваш консультант из Smart Accessories. Готов помочь с MagSafe!",
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текстовые сообщения (простая логика)."""
    text = update.message.text
    if text and ("MagSafe" in text or "хочу" in text):
        # Здесь будет логика Вашего диалогового цепочки
        await update.message.reply_text("Отличный выбор! Перехожу к каталогу и скидкам.")
    else:
        await update.message.reply_text("Я — простой бот. Если у Вас сложный вопрос, лучше нажмите /start и выберите опцию.")


# --- ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ---

def main() -> None:
    """Запускает бота в режиме Long Polling (Опрос)."""
    
    if BOT_TOKEN == "ВАШ_ТОКЕН_ОТ_BOTFATHER":
        logger.error("КРИТИЧЕСКАЯ ОШИБКА: Замените 'ВАШ_ТОКЕН_ОТ_BOTFATHER' на реальный токен!")
        return
    
    # 1. Создание Application
    # В Long Polling не нужен Updater, поэтому .build() работает без ошибок.
    application = Application.builder().token(BOT_TOKEN).build() 

    # 2. Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 3. Запуск в режиме Long Polling
    logger.info("Запуск бота в режиме Long Polling...")
    
    # Этот метод просто начинает опрос Telegram-серверов.
    application.run_polling(poll_interval=3.0) 


if __name__ == '__main__':
    main()
