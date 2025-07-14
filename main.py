import logging
import os

import telegram
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

load_dotenv()

from handle import cancel, help, start

logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main() -> None:
	application = Application.builder().token(os.getenv("TOKEN")).build()

	# REGISTER COMMAND
	application.add_handler(CommandHandler("start", start))
	application.add_handler(CommandHandler("cancel", cancel))
	application.add_handler(CommandHandler("help", help))

	# REGISTER CALLBACK BUTTON
	application.add_handler(CallbackQueryHandler(start, pattern="back"))
	application.add_handler(CallbackQueryHandler(help, pattern="help"))

	application.run_polling(allowed_updates=telegram.Update.ALL_TYPES)


if __name__ == "__main__":
	main()
