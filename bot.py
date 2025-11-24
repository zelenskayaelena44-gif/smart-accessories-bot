from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8270132256:AAELg2DTV0qifcHN4q8uvqrEFy6O75yMPcc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Smart Accessories Bot работает! 😊")

def main():
app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.run_webhook()

if __name__ == "__main__":
    main()
