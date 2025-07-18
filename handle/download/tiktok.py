import os
import uuid

import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

# State untuk ConversationHandler
TIKTOK = range(1)


# ENTRY POINT
async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data.clear()
	button = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]

	send = await context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="""
Silahkan kirimkan link video TikTok yang ingin Anda download:
    """,
		parse_mode="HTML",
		reply_markup=InlineKeyboardMarkup(button),
	)

	context.user_data["message_data"] = send.message_id
	return TIKTOK


# PILIH MEDIA DOWNLOADER
async def tiktok_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		link = update.message.text.strip()
		data = context.user_data.get("message_data")

		tiktok_domains = [
			"https://vt.tiktok.com/",
			"https://www.tiktok.com/",
			"https://vm.tiktok.com/",
			"https://tiktok.com/",
		]

		if not any(link.startswith(domain) for domain in tiktok_domains):
			button = [
				[
					InlineKeyboardButton("Help Menu", callback_data="help"),
					InlineKeyboardButton("Ulangi", callback_data="tiktok"),
				]
			]
			await update.message.reply_text(
				"Pastikan anda memasukan link tiktok dengan benar",
				reply_markup=InlineKeyboardMarkup(button),
			)
			return ConversationHandler.END

		button = [
			[
				InlineKeyboardButton("Video", callback_data="tiktok_video"),
				InlineKeyboardButton("Music", callback_data="tiktok_music"),
			],
			[InlineKeyboardButton("Cancel", callback_data="cancel")],
		]

		if data:
			await context.bot.delete_message(
				chat_id=update.effective_chat.id, message_id=data["message_id"]
			)

		context.user_data["download_link"] = link  # Simpan langsung string link
		# Kirim pesan untuk pilih media
		send = await update.message.reply_text(
			"Pilih media yang ingin di download", reply_markup=InlineKeyboardMarkup(button)
		)

		context.user_data["message_data"] = send.message_id
		return TIKTOK

	except Exception as e:
		await update.message.reply_text("Terjadi kesalahan, silahkan coba lagi.")
		return ConversationHandler.END


# DOWNLOAD TIKTOK MUSIC
async def download_tiktok_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.callback_query
	temp_file = f"assets/audio/{uuid.uuid4()}"

	try:
		await query.answer()

		link = context.user_data.get("download_link")
		message_data = context.user_data.get("message_data")

		if not link:
			await query.edit_message_text("Link tidak ditemukan, silahkan coba lagi.")
			context.user_data.clear()
			return ConversationHandler.END

		button = [
			[
				InlineKeyboardButton("Help menu", callback_data="help_after_download"),
				InlineKeyboardButton("Support me", url="https://tako.id/cliari"),
			]
		]

		# Buat folder jika belum ada
		os.makedirs("assets/video", exist_ok=True)

		# Konfigurasi yt-dlp
		ydl_opts = {
			"format": "bestaudio/best",
			"postprocessors": [
				{
					"key": "FFmpegExtractAudio",
					"preferredcodec": "mp3",
					"preferredquality": "192",
				}
			],
			"outtmpl": temp_file,
			"quiet": True,
		}
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			send = await context.bot.edit_message_text(
				text="Mohon tunggu.......",
				chat_id=update.effective_chat.id,
				message_id=message_data.get("message_id"),
			)

			await context.bot.send_chat_action(
				chat_id=update.effective_chat.id, action="upload_voice"
			)

			info = ydl.extract_info(link, download=True)
			filename = f"{ydl.prepare_filename(info)}.mp3"

			caption = [
				"📹 <b>Video TikTok</b>",
				f"🎵 {info.get('title', 'No caption')}",
				f"👁️ {info.get('view_count', 0):,} views",
				f"❤️ {info.get('like_count', 0):,} likes",
				"",
				"Jangan lupa share bot ini jika menurutmu berguna.",
			]

			await context.bot.delete_message(
				chat_id=update.effective_chat.id, message_id=send.message_id
			)

			await context.bot.send_audio(
				chat_id=update.effective_chat.id,
				audio=open(filename, "rb"),
				title=info.get("title", "TikTok Audio"),
				performer=info.get("uploader", "TikTok"),
				caption="\n".join(caption),
				parse_mode="HTML",
				reply_markup=InlineKeyboardMarkup(button),
			)

			if os.path.exists(filename):
				os.remove(filename)

		context.user_data.clear()
		return ConversationHandler.END

	except yt_dlp.utils.DownloadError as e:
		if os.path.exists(temp_file):
			os.remove(temp_file)
		await query.edit_message_text(
			f"Gagal mendownload audio. Link mungkin tidak valid atau video di-private.: {e}"
		)
	except Exception as e:
		if os.path.exists(temp_file):
			os.remove(temp_file)
		await query.edit_message_text(f"Terjadi kesalahan saat memproses audio.: {e}")
	finally:
		context.user_data.clear()
	return ConversationHandler.END


# DOWNLOAD TIKTOK VIDEO
async def download_tiktok_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.callback_query
	temp_file = f"assets/video/{uuid.uuid4()}.mp4"

	try:
		await query.answer()

		link = context.user_data.get("download_link")
		message_data = context.user_data.get("message_data")

		if not link:
			await query.edit_message_text("Link tidak ditemukan, silahkan coba lagi.")
			context.user_data.clear()
			return ConversationHandler.END

		button = [
			[
				InlineKeyboardButton("Help menu", callback_data="help_after_download"),
				InlineKeyboardButton("Support me", url="https://tako.id/cliari"),
			]
		]

		# Konfigurasi yt-dlp
		ydl_opts = {
			"format": "best",
			"outtmpl": temp_file,
			"quiet": True,
		}

		# Buat folder jika belum ada
		os.makedirs("assets/video", exist_ok=True)

		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			send = await context.bot.edit_message_text(
				text="Mohon tunggu.......",
				chat_id=message_data.get("chat_id"),
				message_id=message_data.get("message_id"),
			)

			await context.bot.send_chat_action(chat_id=query.message.chat.id, action="upload_video")

			info = ydl.extract_info(link, download=True)
			filename = ydl.prepare_filename(info)

			caption = [
				"📹 <b>Video TikTok</b>",
				f"🎵 {info.get('title', 'No caption')}",
				f"👁️ {info.get('view_count', 0):,} views",
				f"❤️ {info.get('like_count', 0):,} likes",
				"",
				"Jangan lupa share bot ini jika menurutmu berguna.",
			]

			await context.bot.delete_message(chat_id=send.chat.id, message_id=send.message_id)

			await context.bot.send_video(
				chat_id=query.message.chat.id,
				video=open(filename, "rb"),
				caption="\n".join(caption),
				parse_mode="HTML",
				reply_markup=InlineKeyboardMarkup(button),
			)

			if os.path.exists(filename):
				os.remove(filename)

		context.user_data.clear()
		return ConversationHandler.END

	except yt_dlp.utils.DownloadError as e:
		await query.edit_message_text(
			"Gagal mendownload video. Link mungkin tidak valid atau video di-private."
		)

	except Exception as e:
		await query.edit_message_text("Terjadi kesalahan saat memproses video.")
	finally:
		if os.path.exists(temp_file):
			os.remove(temp_file)
		context.user_data.clear()
	return ConversationHandler.END
