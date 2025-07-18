import os
import uuid

from PIL import Image
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Conversation states
INPUT_FILE = range(1)


# ENTRY POINT
async def resize(update: Update, context: ContextTypes.DEFAULT_TYPE):
	context.user_data.clear()

	# Kirim pesan bot dan simpan message_id-nya
	sent_message = await context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="Silahkan kirimkan foto",
		reply_markup=InlineKeyboardMarkup(
			[[InlineKeyboardButton("Cancel", callback_data="cancel")]]
		),
	)

	# Simpan message_id bot ke user_data
	context.user_data["message_id"] = sent_message.message_id
	return INPUT_FILE


# PILIH SIZE PHOTO
async def pilih_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
	id = uuid.uuid4()
	os.makedirs("assets/photo", exist_ok=True)
	message = context.user_data.get("message_id")

	# Ambil file dari chat
	file = await update.message.document.get_file()
	# Ambil nama file
	file_name = await update.message.document.file_name

	# Resize
	options = {
		# Icons & Thumbnails
		'16x16': (16, 16),      # Favicons
		'32x32': (32, 32),      # Taskbar icons
		'64x64': (64, 64),      # Small app icons
		'128x128': (128, 128),  # Medium thumbnails
		
		# Profile Images
		'150x150': (150, 150),  # Small avatars
		'256x256': (256, 256),  # Medium profile pictures
		'400x400': (400, 400),  # HD profile images
		
		# Social Media
		'600x600': (600, 600),      # Instagram posts
		'1080x1080': (1080, 1080),  # Instagram square HQ
		'1200x630': (1200, 630),    # Facebook/LinkedIn links (1.91:1)
		
		# Web Content
		'800x600': (800, 600),      # Blog images (4:3)
		'1024x768': (1024, 768),    # Standard display (4:3)
		'1280x720': (1280, 720),    # HD video thumbnails (16:9)
		'1920x1080': (1920, 1080),  # Full HD (16:9)
		
		# Mobile & Stories
		'1080x1920': (1080, 1920),  # Instagram/WhatsApp stories (9:16)
		'1242x2688': (1242, 2688),   # iPhone X/XS display
		
		# Print Sizes (300 DPI equivalent)
		'2480x3508': (2480, 3508),  # A4 paper (21×29.7cm)
		'2550x3300': (2550, 3300),  # US Letter (8.5×11in)
		
		# Large Formats
		'3840x2160': (3840, 2160),  # 4K UHD
		'6016x3384': (6016, 3384),  # 6K resolution
		
		# Banner Ads
		'728x90': (728, 90),        # Leaderboard banner
		'300x250': (300, 250),      # Medium rectangle
		
		# Email Headers
		'600x200': (600, 200),      # Email header (3:1)
		
		# Custom Aspect Ratios
		'1200x628': (1200, 628),    # Twitter header (~2:1)
		'1600x900': (1600, 900)     # YouTube channel art
	}

	# Kirim pesan untuk memilih ukuran
	pilih_ukuran = await context.bot.edit_message_text(
		chat_id=update.effective_chat.id,
		message_id=message,
		text="Pilih ukuran gambar",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(f"{key}", callback_data=f"{key}")
					for key in options.keys()
				]
			]
		),
	)

	# message saving file
	saving_text = await context.bot.edit_message_text(
		chat_id=update.effective_chat.id, message_id=pilih_ukuran.message_id, text="Saving file......"
	)

	# Temp file
	path_file = f"assets/photo/{id + file_name}"
	await file.download_to_drive(path_file)

	context.user_data['data_photo'] = {
		'message_id': saving_text.message_id,
		'path_file': path_file,
		'nama_file': file_name
	}

	return INPUT_FILE