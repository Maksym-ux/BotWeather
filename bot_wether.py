import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

from telegram.constants import BOT_API_VERSION

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")  # заміни своїм токеном
WEATHER_API_KEY = ("BOT_WEATHER_API_KEY")  # встав свій API ключ з openweathermap.org

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_weather(city: str):
    url = f"http://maps.openweathermap.org/maps/2.0/weather/?appid={WEATHER_API_KEY}&units=metric&lang=ua"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                name = data["name"]
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                weather = data["weather"][0]["description"]
                wind = data["wind"]["speed"]
                return f"🌍 Місто: {name}\n🌡 Температура: {temp}°C\n🤔 Відчувається як: {feels_like}°C\n🌥 Погода: {weather}\n💨 Вітер: {wind} м/с"
            else:
                return None


@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привіт! Введи назву міста, і я скажу тобі погоду 🌤")


@dp.message()
async def handle_city(message: Message):
    city = message.text.strip()
    weather_info = await get_weather(city)
    if weather_info:
        await message.answer(weather_info)
    else:
        await message.answer("⚠️ Місто не знайдено або помилка API. Спробуй ще раз.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
