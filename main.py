import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Load the token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Main menu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💱 Exchange Rates"), KeyboardButton(text="🛡 Hedge")],
        [KeyboardButton(text="👨‍💬 Chat with Admin"), KeyboardButton(text="🌐 Language")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Welcome! Choose an action:", reply_markup=main_menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
