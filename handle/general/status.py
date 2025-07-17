import psutil, asyncio, threading

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


# STATUS COMMANDS
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
	query = update.callback_query
	app = context.application

	# Dapatkan antrian user
	queue_size = app.update_queue.qsize()

	caption = f"""
💻 <b>System Status Report</b>

📊 <b>Resource Usage</b>
- CPU: {psutil.cpu_percent()} %
- RAM: {psutil.virtual_memory().percent} %
- DISK: {psutil.disk_usage("/").percent} %

🤖 <b>Bot Metrics</b>
- Active Task: {len(asyncio.all_tasks())}
- Event Loop: {asyncio.get_event_loop().is_running() and "Running" or "Stopped"}
- Thread Count: {threading.active_count()}

🚦 <b>Queue Status</b>
- User in queue: {queue_size}
- Max queue size: {app.update_queue.maxsize}
- Active concurrent user: {app.concurrent_updates}

🟢 Status Bot: @NexusUpdatee
"""

	button = [
		[
			InlineKeyboardButton("Help menu", callback_data="help"),
			InlineKeyboardButton("🧧 Donate", url="https://tako.id/cliari"),
		]
	]

	if query and query.data == "status":
		await update.callback_query.edit_message_text(
			text=caption, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(button)
		)
	else:
		await update.message.reply_text(
			text=caption, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(button)
		)
