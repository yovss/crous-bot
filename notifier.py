from telegram import Bot
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)

async def send_message(chat_id, text):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(e)