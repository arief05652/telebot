from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import yt_dlp
import uuid
import os
import io

# State untuk ConversationHandler
ONE = range(1)


async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
	button = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]
	query = update.callback_query

	if query and query.data == "tiktok":
		await context.bot.send_message(
			chat_id=query.message.chat.id,
			text="Silahkan kirimkan link video TikTok yang ingin Anda download:",
			reply_markup=InlineKeyboardMarkup(button),
		)
	else:
		await update.message.reply_text(
			text="Silahkan kirimkan link video TikTok yang ingin Anda download:",
			reply_markup=InlineKeyboardMarkup(button),
		)
	return ONE


async def download_tiktok_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.callback_query
	info = context.user_data["download_link"]

	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help_after_download"),
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		]
	]

	try:
		# Hapus pesan tombol
		await context.bot.delete_message(
			chat_id=query.message.chat.id, message_id=query.message.message_id
		)

		# Konfigurasi yt-dlp yang benar
		ydl_opts = {
			"format": "bestaudio/best",
			"postprocessors": [
				{
					"key": "FFmpegExtractAudio",
					"preferredcodec": "mp3",
					"preferredquality": "192",
				}
			],
			"outtmpl": f"assets/video/{uuid.uuid4()}",  # Tanpa ekstensi
			"keepvideo": False,
			"quiet": True,
		}

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			await context.bot.send_chat_action(
				chat_id=update.effective_chat.id,
				action="upload_voice"
			)
			info = ydl.extract_info(info["link"], download=True)

			# File akhir akan selalu .mp3 karena preferredcodec
			filename = f"{ydl.prepare_filename(info)}.mp3"

			# Kirim audio
			await context.bot.send_audio(
				chat_id=query.message.chat.id,
				audio=open(filename, "rb"),
				title="Nexus music",
				performer="TikTok",
				duration=int(info.get("duration", 0)),
				reply_markup=InlineKeyboardMarkup(button),
			)

			# Bersihkan file
			os.remove(filename)
			context.user_data.clear()

	except Exception as e:
		await context.bot.send_message(
			chat_id=query.message.chat.id, text=f"❌ Error: {str(e)[:200]}... (truncated)"
		)


async def download_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
	link = update.message.text

	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help_after_download"),
			InlineKeyboardButton("Download music", callback_data="tiktok_music"),
		],
		[
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		],
	]

	try:
		ydl_opts = {
				"format": "best", 
				"quiet": True, 
				"outtmpl": f"assets/video/{uuid.uuid4()}"
		}

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			await context.bot.send_chat_action(
				chat_id=update.effective_chat.id,
				action="upload_video"
			)
			info = ydl.extract_info(link, download=True)
			filename = ydl.prepare_filename(info)
			caption = [
				"<b>Information</b>",
				"",
				f"Caption: {info['title']}",
				f"View: {float(info['view_count']):,.0f}",
				f"Like: {float(info['like_count']):,.0f}",
				f"Repost: {float(info['repost_count']):,.0f}",
			]
			context.user_data["download_link"] = {"link": link}
			await update.message.reply_video(
				video=open(filename, "rb"),
				caption="\n".join(caption),
				parse_mode="HTML",
				reply_markup=InlineKeyboardMarkup(button),
			)
			os.remove(filename)
	except Exception as e:
		await update.message.reply_text(f"Error: {e}")

	return ConversationHandler.END
