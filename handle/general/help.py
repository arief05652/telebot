import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ..list_assets import gif_help


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message_lines = [
		"Berikut adalah list perintah yang tersedia:",
		"",
		"📃 <b>PDF commands</b>",
		"- /docxtopdf - Konversi file docx ke pdf",
		"- /pdftodocx - Konversi file pdf ke docx",
		"- /reducepdf - Perkecil ukuran file pdf",
		"- /stamppdf - Menambahkan watermark ke file pdf",
		"- /imgtopdf - Konversi gambar ke pdf",
		"",
		"📱 <b>Video commands</b>",
		"- /tiktok - Download video/audio tiktok",
		"- /youtube - Download video youtube",
		"",
		"✂️ <b>Convert commands</b>",
		"- /resizeimg - Mengubah ukuran gambar",
		"- /imgtosticker - Mengubah gambar menjadi sticker",
		"",
		"🔍 Ketik /help untuk melihat daftar perintah lengkap",
		"",
		"📜 <b>Note</b>",
		"- Bot ini tidak menyimpan data yang Anda kirimkan, namun kami akan memeriksa apakah Anda mengirimkan file yang valid.",
		"- Jika Anda tidak memahami perintah yang diberikan, Anda dapat menggunakan perintah /cancel untuk membatalkan perintah.",
		"",
		"🤖 Status Bot: @NexusStatus",
		"🧧 Donate: https://tako.id/cliari",
	]

	# Buat inline buttons
	buttons_callback = [
		[
			InlineKeyboardButton("Back", callback_data="back"),
		],
		[
			InlineKeyboardButton("Docx to PDF", callback_data="docxtopdf"),
			InlineKeyboardButton("PDF to Docx", callback_data="pdftodocx"),
			InlineKeyboardButton("Reduce PDF", callback_data="reducepdf"),
		],
		[
			InlineKeyboardButton("Stamp PDF", callback_data="stamppdf"),
			InlineKeyboardButton("Image to PDF", callback_data="imgtopdf"),
			InlineKeyboardButton("TikTok", callback_data="tiktok"),
		],
		[
			InlineKeyboardButton("YouTube", callback_data="youtube"),
			InlineKeyboardButton("Resize Image", callback_data="resizeimg"),
			InlineKeyboardButton("Image to Sticker", callback_data="imgtosticker"),
		]
	]

	buttons = [
		[
			InlineKeyboardButton("Docx to PDF", callback_data="docxtopdf"),
			InlineKeyboardButton("PDF to Docx", callback_data="pdftodocx"),
			InlineKeyboardButton("Reduce PDF", callback_data="reducepdf"),
		],
		[
			InlineKeyboardButton("Stamp PDF", callback_data="stamppdf"),
			InlineKeyboardButton("Image to PDF", callback_data="imgtopdf"),
			InlineKeyboardButton("TikTok", callback_data="tiktok"),
		],
		[
			InlineKeyboardButton("YouTube", callback_data="youtube"),
			InlineKeyboardButton("Resize Image", callback_data="resizeimg"),
			InlineKeyboardButton("Image to Sticker", callback_data="imgtosticker"),
		]
	]

	markup_callback = InlineKeyboardMarkup(buttons_callback)
	reply_markup = InlineKeyboardMarkup(buttons)

	if update.callback_query:
		await update.callback_query.edit_message_caption(
			caption="\n".join(message_lines), parse_mode="HTML", reply_markup=markup_callback
		)
	else:
		await update.message.reply_animation(
			animation="".join(random.choice(gif_help)),
			caption="\n".join(message_lines),
			parse_mode="HTML",
			reply_markup=reply_markup,
		)
