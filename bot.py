from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Привет! Я Smart Accessories Bot.")

app = Application.builder().token("ТОКЕН_СЮДА").build()
app.add_handler(CommandHandler("start", start))

app.run_polling(8270132256:AAELg2DTV0qifcHN4q8uvqrEFy6O75yMPcc)
