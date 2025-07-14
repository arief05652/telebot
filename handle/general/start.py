import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from ..list_assets import gif_start


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
🧧 Donate: https://tako.id/cliari
"""

	# Buat inline buttons
	buttons = [
		[
			InlineKeyboardButton("📋 Help", callback_data="help"),
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		]
	]
	reply_markup = InlineKeyboardMarkup(buttons)

	if update.callback_query:
		await update.callback_query.edit_message_caption(
			caption=caption,
			parse_mode="HTML",
			reply_markup=reply_markup,
		)
	else:
		# Kirim GIF dengan caption + buttons
		await update.message.reply_animation(
			animation=random.choice(gif_start),
			caption=caption,
			parse_mode="HTML",
			reply_markup=reply_markup,
		)