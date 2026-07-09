import asyncio

from scraper import get_available_rooms
from telegram_sender import send_to_all
from database import room_exists, add_room, get_subscribers


async def check():
    print("Checking for new CROUS rooms...")

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

            await send_to_all(subscribers, message)
    else:
        print("No new rooms found.")


async def main():
    while True:
        try:
            await check()
        except Exception as e:
            print(e)

        print("Sleeping for 5 minutes...")
        await asyncio.sleep(300)  # 5 minutes


if __name__ == "__main__":
    asyncio.run(main())