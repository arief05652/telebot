from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help"),
			InlineKeyboardButton("Ulangi", callback_data="tiktok"),
		]
	]

	if update.callback_query:
		await update.callback_query.edit_message_text(
			text=f"Berhasil membatalkan perintah",
			reply_markup=InlineKeyboardMarkup(button),
		)
		return ConversationHandler.END
	else:
		await update.callback_query.edit_message_text(
			text=f"Berhasil membatalkan perintah",
			reply_markup=InlineKeyboardMarkup(button),
		)
		return ConversationHandler.END
