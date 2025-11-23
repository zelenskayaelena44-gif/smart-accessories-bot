from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "8270132256:AAELg2DTV0qifcHN4q8uvqrEFy6O75yMPcc"

def start(update, context):
    update.message.reply_text("Привет! Smart Accessories Bot работает :)")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
