from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help"),
		]
	]

	if update.callback_query:
		context.user_data.clear()  # clear data
		await update.callback_query.edit_message_text(  # edit chat
			text=f"Berhasil membatalkan perintah",
			reply_markup=InlineKeyboardMarkup(button),
		)
		return ConversationHandler.END
	else:
		context.user_data.clear()
		await update.callback_query.edit_message_text(
			text=f"Berhasil membatalkan perintah",
			reply_markup=InlineKeyboardMarkup(button),
		)
		return ConversationHandler.END
