import asyncio
from telegram import Bot

async def main():
    bot = Bot(token="7994962595:AAGOZdezJAetEVJPCpbOVqAds7AYaypWlRY")
    try:
        chat = await bot.get_chat(6170655291)
        print("First Name:", chat.first_name)
        print("Last Name:", chat.last_name)
        print("Username:", chat.username)
    except Exception as e:
        print("Could not fetch user:", e)

asyncio.run(main())
