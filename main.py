import logging
import os

import telegram
from dotenv import load_dotenv
from telegram.ext import (
	Application,
	CommandHandler,
	CallbackQueryHandler,
	ConversationHandler,
	MessageHandler,
	filters,
)

load_dotenv()

from handle import cancel, help, start, tiktok, download_tiktok_video, download_tiktok_music

logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

ONE = range(1)


def main() -> None:
	application = Application.builder().token(os.getenv("TOKEN")).build()

	# REGISTER COMMAND
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("help", help))

	# REGISTER CALLBACK BUTTON
	application.add_handler(CallbackQueryHandler(start, pattern="start"))
	application.add_handler(CallbackQueryHandler(help, pattern="help"))
	application.add_handler(CallbackQueryHandler(download_tiktok_music, pattern="^tiktok_music$"))

	# REGISTER CONVERSATION
	tiktok_conv = ConversationHandler(
		entry_points=[
			CommandHandler("tiktok", tiktok),
			CallbackQueryHandler(tiktok, pattern="^tiktok$"),
		],
		states={
			ONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok_video)],
		},
		fallbacks=[
			CallbackQueryHandler(cancel, pattern="cancel"),
			CommandHandler("cancel", cancel),
		],
	)
	application.add_handler(tiktok_conv)

	application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)


if __name__ == "__main__":
	main()
