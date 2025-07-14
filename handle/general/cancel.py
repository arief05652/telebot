from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text(
		text="Berhasil membatalkan perintah", reply_markup=ReplyKeyboardRemove()
	)
