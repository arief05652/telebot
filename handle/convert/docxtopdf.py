import os
import uuid

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# Conversation states
INPUT_FILE = range(1)


async def docx_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data.clear()

	# Kirim pesan bot dan simpan message_id-nya
	sent_message = await context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="Silahkan kirimkan file '.docx'",
		reply_markup=InlineKeyboardMarkup(
			[[InlineKeyboardButton("Cancel", callback_data="cancel")]]
		),
	)

	# Simpan message_id bot ke user_data
	context.user_data["message_id"] = sent_message.message_id
	return INPUT_FILE


async def cv_docx_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
	os.makedirs("assets/document", exist_ok=True)
	message = context.user_data.get('message_id')

	# Hapus pesan bot sebelumnya
	if message:
		await context.bot.delete_message(
			chat_id=update.effective_chat.id, message_id=message
		)
	# Ambil file dari chat yang dikirimkan
	file = await update.message.document.get_file()
	# Ambil nama file
	file_name = update.message.document.file_name

	id = uuid.uuid4()

	# Cek apakah yang dikirimkn ber-ektensi .docx
	if file_name.endswith(".docx"):
		# Kirim pesan konversi dan simpan message_id-nya
		processing_msg = await context.bot.send_message(
			chat_id=update.effective_chat.id, text="Converting DOCX to PDF..."
		)
		context.user_data["processing_msg_id"] = processing_msg.message_id

		# Template file
		temp_docx = os.path.abspath(f"assets/document/{id}.docx")
		temp_pdf = os.path.abspath(f"assets/document/{id}.pdf")

		# Download file yang dikirimkan user
		await file.download_to_drive(temp_docx)
		# Jalankan libre untuk convert
		os.system(
			f"libreoffice --headless --nologo --norestore --convert-to pdf --outdir {os.path.abspath('assets/document')} {temp_docx}"
		)

		if not os.path.exists(temp_pdf):
			await context.bot.send_message(
				chat_id=update.effective_chat.id, text="Gagal mengkonversi dokumen."
			)
			return ConversationHandler.END

		# Hapus pesan "Converting..." sebelum kirim hasil
		await context.bot.delete_message(
			chat_id=update.effective_chat.id, message_id=processing_msg.message_id
		)

		button = [
			[
				InlineKeyboardButton("Help menu", callback_data="help_after_download"),
				InlineKeyboardButton("Support me", url="https://tako.id/cliari"),
			]
		]

		await context.bot.send_document(
			chat_id=update.effective_chat.id,
			document=open(temp_pdf, "rb"),
			filename=str(os.path.splitext(file_name)[0]) + ".pdf",
			reply_markup=InlineKeyboardMarkup(button),
			caption="Jangan lupa share bot ini jika menurutmu berguna.",
		)

		os.remove(temp_docx)
		os.remove(temp_pdf)

	return ConversationHandler.END
