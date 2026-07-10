import asyncio
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
    room_exists,
    add_room
)
from scraper import get_available_rooms

# ==========================================
# 1. BOT COMMAND HANDLERS
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_subscriber(chat_id)
    await update.message.reply_text("✅ You are now subscribed to CROUS alerts!")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    remove_subscriber(chat_id)
    await update.message.reply_text("❌ You have been unsubscribed.")

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

    await update.message.reply_text(f"🏠 {len(rooms)} room(s) currently available:")

    for room in rooms:
        message = (
            f"🏢 {room['title']}\n"
            f"💶 {room['price']}\n\n"
            f"{room['url']}"
        )
        await update.message.reply_text(message, disable_web_page_preview=True)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")


# ==========================================
# 2. BACKGROUND CHECKER (Replaces old while loop)
# ==========================================

async def check_rooms(context: ContextTypes.DEFAULT_TYPE):
    """This function will run automatically in the background every 5 minutes."""
    print("Checking for new CROUS rooms...")
    
    try:
        rooms = await get_available_rooms()
        subscribers = get_subscribers()

        new_rooms = []

        for room in rooms:
            room_id = room["url"]
            if not room_exists(room_id):
                add_room(room_id)
                new_rooms.append(room)

        if new_rooms:
            print(f"{len(new_rooms)} new room(s) found!")

            for room in new_rooms:
                message = (
                    f"🏠 New CROUS accommodation!\n\n"
                    f"🏢 {room['title']}\n"
                    f"💶 {room['price']}\n\n"
                    f"{room['url']}"
                )

                # Send to all subscribers using the context.bot directly
                for chat_id in subscribers:
                    try:
                        await context.bot.send_message(
                            chat_id=chat_id, 
                            text=message,
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        print(f"Failed to send message to {chat_id}: {e}")
        else:
            print("No new rooms found.")
            
    except Exception as e:
        print(f"An error occurred while checking for rooms: {e}")


# ==========================================
# 3. MAIN APPLICATION STARTUP
# ==========================================

def main():
    # Initialize application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("showall", showall))
    
    # 🌟 Add the background job 🌟
    # interval=300 sets it to check every 300 seconds (5 mins)
    # first=10 tells it to do the very first check 10 seconds after the bot boots up
    app.job_queue.run_repeating(check_rooms, interval=5, first=1)

    print("🤖 Bot started...")
    
    # Start bot polling
    app.run_polling()

if __name__ == "__main__":
    main()