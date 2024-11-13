from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to Plasec!')

if __name__ == '__main__':
    application = ApplicationBuilder(os.getenv('YOUR_TELEGRAM_BOT_TOKEN_BETA')).token().build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
