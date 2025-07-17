import logging
import os
import asyncio

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
	status,
	pdf_to_docx,
	cv_pdf_to_docx,
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
	application = (
		Application.builder()
		.token(os.getenv("TOKEN"))
		.concurrent_updates(25)  # maks interaksi bersamaan
		.http_version("2")  # http version
		.pool_timeout(15)  # timeout 15 dtk ketika sistem overload
		.read_timeout(15)  # timeout 15 dtk ketika network overload
		.update_queue(asyncio.Queue(30))  # set maks antrian
		.build()
	)

	# REGISTER CONVERSATION HANDLER FIRST (SPECIFIC)
	tiktok_conv = ConversationHandler(  # TIKTOK
		allow_reentry=True,
		block=False,
		entry_points=[
			CallbackQueryHandler(tiktok, pattern="^tiktok$"),
			CommandHandler("tiktok", tiktok),
		],
		states={
			TIKTOK: [
				MessageHandler(filters.TEXT & ~filters.COMMAND, tiktok_media, block=False),
			],
		},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="^cancel$"),
			CommandHandler("cancel", cancel),
		],
	)

	docx_to_pdf_conv = ConversationHandler(  # CV DOCX TO PDF
		allow_reentry=True,
		block=False,
		entry_points=[
			CallbackQueryHandler(docx_to_pdf, pattern="^docxtopdf$"),
			CommandHandler("docxtopdf", docx_to_pdf),
		],
		states={INPUT_FILE: [MessageHandler(filters.Document.ALL, cv_docx_to_pdf, block=False)]},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="^cancel$"),
			CommandHandler("cancel", cancel),
		],
	)

	pdf_to_docx_conv = ConversationHandler(  # CV PDF TO DOCX
		allow_reentry=True,
		block=False,
		entry_points=[
			CallbackQueryHandler(pdf_to_docx, pattern="^pdftodocx$"),
			CommandHandler("pdftodocx", pdf_to_docx),
		],
		states={INPUT_FILE: [MessageHandler(filters.Document.ALL, cv_pdf_to_docx, block=False)]},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="^cancel$"),
			CommandHandler("cancel", cancel),
		],
	)

	#  REGISTER CONVERSATION
	application.add_handlers([tiktok_conv, docx_to_pdf_conv, pdf_to_docx_conv])

	# REGISTER SPECIFIC CALLBACK HANDLERS
	application.add_handlers(
		[
			CallbackQueryHandler(download_tiktok_music, pattern="^tiktok_music$", block=False),
			CallbackQueryHandler(download_tiktok_video, pattern="^tiktok_video$", block=False),
			CallbackQueryHandler(status, pattern="^status$", block=False),
		]
	)

	# REGISTER GENERAL COMMANDS
	application.add_handlers(
		[
			CommandHandler("start", start, block=False),
			CommandHandler("help", help, block=False),
			CallbackQueryHandler(start, pattern="^start$", block=False),
			CallbackQueryHandler(help, pattern="^(help|help_after_download)$", block=False),
		]
	)

	application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)


if __name__ == "__main__":
	main()
