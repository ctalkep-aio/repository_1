from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

text1 = "1-ая страница"
text2 = "2-ая страница"
text3 = "3-ья страница"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет, это каталог бот, напиши /pages, чтобы посмотреть страницы")

@dp.message(Command("pages"))
async def pages(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вперед", callback_data="next_1"),
                InlineKeyboardButton(text="Назад", callback_data="prev_1")
            ]
        ]
    )
    await message.answer(text1, reply_markup=None)

@dp.callback_query()
async def change_page(callback: types.CallbackQuery):
    action, page_num = callback.data.split("_")
    page_num = int(page_num)

    if action == "next" and page_num == 1:
        new_text = text2
        new_page = 2
    elif action == "next" and page_num == 2:
        new_text = text3
        new_page = 3
    elif action == "prev" and page_num == 2:
        new_text = text1
        new_page = 1
    elif action == "prev" and page_num == 3:
        new_text = text2
        new_page = 2
    else:
        await callback.answer("Ты уже на этой странице!")
        return

    # Создаём новую клавиатуру для новой страницы
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вперед", callback_data=f"next_{new_page}"),
                InlineKeyboardButton(text="Назад", callback_data=f"prev_{new_page}")
            ]
        ]
    )

    await callback.message.edit_text(new_text, reply_markup=keyboard)
    await callback.answer(f"Страница {new_page}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
