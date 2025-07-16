import logging
import os

import telegram
from dotenv import load_dotenv
from telegram.ext import (
	Application,
	CallbackQueryHandler,
	CommandHandler,
	ConversationHandler,
	MessageHandler,
	filters,
)

load_dotenv()

from handle import (
	cancel,
	cv_docx_to_pdf,
	docx_to_pdf,
	download_tiktok_music,
	download_tiktok_video,
	help,
	start,
	tiktok,
	tiktok_media,
)

# LOOGGING BOT
logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# STATE CONVERSATION
TIKTOK = range(1)
INPUT_FILE = range(1)


def main() -> None:
	# BUILD BOT
	application = Application.builder().token(os.getenv("TOKEN")).build()

	# REGISTER CONVERSATION HANDLER FIRST (SPECIFIC)
	tiktok_conv = ConversationHandler(  # TIKTOK
		allow_reentry=True,
		entry_points=[
			CallbackQueryHandler(tiktok, pattern="^tiktok$"),
			CommandHandler("tiktok", tiktok),
		],
		states={
			TIKTOK: [
				MessageHandler(filters.TEXT & ~filters.COMMAND, tiktok_media),
			],
		},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="^cancel$"),
			CommandHandler("cancel", cancel),
		],
	)

	docx_to_pdf_conv = ConversationHandler(  # CV DOCX TO PDF
		allow_reentry=True,
		entry_points=[
			CallbackQueryHandler(docx_to_pdf, pattern="^docxtopdf$"),
			CommandHandler("docxtopdf", docx_to_pdf),
		],
		states={INPUT_FILE: [MessageHandler(filters.Document.DOCX, cv_docx_to_pdf)]},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="^cancel$"),
			CommandHandler("cancel", cancel),
		],
	)

	#  REGISTER CONVERSATION
	application.add_handlers([tiktok_conv, docx_to_pdf_conv])

	# REGISTER SPECIFIC CALLBACK HANDLERS
	application.add_handlers(
		[
			CallbackQueryHandler(download_tiktok_music, pattern="^tiktok_music$"),
			CallbackQueryHandler(download_tiktok_video, pattern="^tiktok_video$"),
		]
	)

	# REGISTER GENERAL COMMANDS
	application.add_handlers(
		[
			CommandHandler("start", start),
			CommandHandler("help", help),
			CallbackQueryHandler(start, pattern="^start$"),
			CallbackQueryHandler(help, pattern="^(help|help_after_download)$"),
		]
	)

	application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)


if __name__ == "__main__":
	main()
