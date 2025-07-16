from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

DOWNLOAD = range(1)


# HELP COMMANDS
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data.clear()
	query = update.callback_query

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
	]

	# Buat inline buttons
	buttons_callback = [
		[
			InlineKeyboardButton("Start menu", callback_data="start"),
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
		],
		[
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		],
	]

	markup_callback = InlineKeyboardMarkup(buttons_callback)

	if query and query.data == "help":  # edit chat
		await query.edit_message_text(
			text="\n".join(message_lines), parse_mode="HTML", reply_markup=markup_callback
		)
		return ConversationHandler.END
	elif query and query.data == "help_after_download":  # kirim chat baru
		await context.bot.send_message(
			chat_id=query.message.chat.id,
			text="\n".join(message_lines),
			parse_mode="HTML",
			reply_markup=markup_callback,
		)
		return ConversationHandler.END
	else:
		await update.message.reply_text(
			text="\n".join(message_lines),
			parse_mode="HTML",
			reply_markup=markup_callback,
		)
		return ConversationHandler.END
