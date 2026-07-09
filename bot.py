from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from database import (
    add_subscriber,
    remove_subscriber,
    get_subscribers,
)
from scraper import get_available_rooms

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    add_subscriber(chat_id)

    await update.message.reply_text(
        "✅ You are now subscribed to CROUS alerts!"
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    remove_subscriber(chat_id)

    await update.message.reply_text(
        "❌ You have been unsubscribed."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subscribers = len(get_subscribers())

    await update.message.reply_text(
        f"""🤖 CROUS Notifier

Commands:
/start - Subscribe
/stop - Unsubscribe
/help - Show help
/test - Test the bot
/showall - Show all available rooms
Subscribers: {subscribers}
"""
    )

async def showall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Checking CROUS...")

    rooms = await get_available_rooms()

    if not rooms:
        await update.message.reply_text("❌ No rooms available right now.")
        return

    await update.message.reply_text(
        f"🏠 {len(rooms)} room(s) currently available:"
    )

    for room in rooms:
        message = (
            f"🏢 {room['title']}\n"
            f"💶 {room['price']}\n\n"
            f"{room['url']}"
        )

        await update.message.reply_text(
            message,
            disable_web_page_preview=True,
        )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot is working!"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("showall", showall))
    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()