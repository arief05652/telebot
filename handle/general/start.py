from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	# Pesan caption
	caption = """
Selamat datang! Saya adalah NexusBot yang siap membantu Anda.

✨ <b>Fitur Utama:</b>
- Download video dari TikTok dan YouTube
- Konversi file DOCX atau PDF
- Tools praktis sehari-hari

🔍 Ketik /help untuk melihat daftar perintah lengkap

🤖 Status Bot: @NexusStatus
"""

	# Buat inline buttons
	buttons = [
		[
			InlineKeyboardButton("Help menu", callback_data="help"),
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		]
	]
	reply_markup = InlineKeyboardMarkup(buttons)
	query = update.callback_query

	if query and query.data == "start":  # pattern callback
		await query.answer()
		await update.callback_query.edit_message_text(
			text=caption,
			parse_mode="HTML",
			reply_markup=reply_markup,
		)
	else:
		# Kirim GIF dengan caption + buttons
		await update.message.reply_text(
			text=caption,
			parse_mode="HTML",
			reply_markup=reply_markup,
		)
