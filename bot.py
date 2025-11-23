from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

BOT_TOKEN = "82780123256:AAkLg2DTVBqifcHN4a8quvqzEFy0675yMPc"   # ← твой токен можно оставить тут

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Smart Accessories Bot работает :)")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()
