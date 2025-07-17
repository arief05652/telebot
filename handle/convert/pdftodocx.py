import os
import uuid

from pdf2docx import Converter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# Conversation states
INPUT_FILE = range(1)


async def pdf_to_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data.clear()

	# Kirim pesan bot dan simpan message_id-nya
	sent_message = await context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="Silahkan kirimkan file '.pdf'",
		reply_markup=InlineKeyboardMarkup(
			[[InlineKeyboardButton("Cancel", callback_data="cancel")]]
		),
	)

	# Simpan message_id bot ke user_data
	context.user_data["message_id"] = sent_message.message_id
	return INPUT_FILE


async def cv_pdf_to_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
	os.makedirs("assets/document", exist_ok=True)
	message = context.user_data.get("message_id")

	# Hapus pesan bot sebelumnya
	if message:
		await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message)
	# Ambil file dari chat yang dikirimkan
	file = await update.message.document.get_file()
	# Ambil nama file
	file_name = update.message.document.file_name

	id = uuid.uuid4()

	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help_after_download"),
			InlineKeyboardButton("Support me", url="https://tako.id/cliari"),
		]
	]

	# Cek apakah yang dikirimkn ber-ektensi .docx
	if not file_name.endswith(".pdf"):
		await context.bot.edit_message_text(
			chat_id=update.effective_chat.id,
			message_id=message,
			text="Pastikan file harus berbentuk PDF",
			reply_markup=InlineKeyboardMarkup(button),
		)
		return ConversationHandler.END
	else:
		# Kirim pesan konversi dan simpan message_id-nya
		processing_msg = await context.bot.send_message(
			chat_id=update.effective_chat.id, text="Converting PDF to DOCX..."
		)
		context.user_data["processing_msg_id"] = processing_msg.message_id

		# Template file
		temp_pdf = os.path.abspath(f"assets/document/{id}.pdf")
		temp_docx = os.path.abspath(f"assets/document/{id}.docx")

		# Download file yang dikirimkan user
		await file.download_to_drive(temp_pdf)

		# Jalankan converter
		cv = Converter(temp_pdf)
		cv.convert(temp_docx, multi_processing=True, layout_analysis=True, tables=True, images=True)
		cv.close()

		# Hapus pdf ketika sudah di convert
		os.remove(temp_pdf)

		if not os.path.exists(temp_docx):
			await context.bot.send_message(
				chat_id=update.effective_chat.id, text="Gagal mengkonversi dokumen."
			)
			return ConversationHandler.END

		# Hapus pesan "Converting..." sebelum kirim hasil
		await processing_msg.delete()

		await context.bot.send_chat_action(
			chat_id=update.effective_chat.id, action="upload_document"
		)

		await context.bot.send_document(
			chat_id=update.effective_chat.id,
			document=open(temp_docx, "rb"),
			filename=str(os.path.splitext(file_name)[0]) + ".docx",
			reply_markup=InlineKeyboardMarkup(button),
			caption="Jangan lupa share bot ini jika menurutmu berguna.",
		)

		os.remove(temp_docx)

		return ConversationHandler.END
