import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

API_TOKEN = "7705891566:AAETdc4uIOJJXDeGPw9jKOiTy-A7SSjkasQ"
ADMIN_ID = 7398183328

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    buttons = [
        [KeyboardButton(text="🚗 ШЫМБАЙ ➡️ НӨКІС")],
        [KeyboardButton(text="🚕 НӨКІС ➡️ ШЫМБАЙ")],
        [KeyboardButton(text="📞 Телефон номеримди жибериу", request_contact=True)],
        [KeyboardButton(text="📍 Мәнзилимди жибериу", request_location=True)],
    ]
    if message.from_user.id == ADMIN_ID:
        buttons.append([KeyboardButton(text="📊 Статистика")])

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Таңлаңыз:", reply_markup=markup)

@dp.message()
async def handle_all(message: types.Message):
    if message.contact:
        await bot.send_message(
            ADMIN_ID,
            f"📞 Жаңа нөмір:\n👤 {message.from_user.full_name}\n📱 {message.contact.phone_number}"
        )
        await message.answer("✅ Телефон нөміріңіз қабылданды!", reply_markup=ReplyKeyboardRemove())
    elif message.location:
        await bot.send_message(
            ADMIN_ID,
            f"📍 Жаңа локация:\n👤 {message.from_user.full_name}\n🌍 https://maps.google.com/?q={message.location.latitude},{message.location.longitude}"
        )
        await message.answer("✅ Локацияңыз қабылданды!", reply_markup=ReplyKeyboardRemove())
    elif message.text in ["🚗 ШЫМБАЙ ➡️ НӨКІС", "🚕 НӨКІС ➡️ ШЫМБАЙ"]:
        await bot.send_message(ADMIN_ID, f"🚖 Бағыт таңдалды: {message.text}\n👤 {message.from_user.full_name}")
        await message.answer("📍 Енді локация мен нөміріңізді жіберіңіз.")
    elif message.text == "📊 Статистика" and message.from_user.id == ADMIN_ID:
        await message.answer("📊 Статистика әзірге қосылмаған.")
    else:
        await message.answer("🤖 Буйыртпа ушин /start ты басыңыз.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
