from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
import logging
from quart import Quart, request
from database import get_joke

TOKEN = "7840680184:AAFfkLbKJQinFyKwlz4Os82Y12on7rRGBIU"  # Укажи свой токен бота
WEBHOOK_URL = "https://67e6-185-200-107-86.ngrok-free.app/webhook/"  # Полный URL вебхука
WEBHOOK_PATH = "/webhook/"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём кнопки
buttons = ["Вовочка", "Штирлиц", "Национальности", "Всё на свете"]
keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=b)] for b in buttons], resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    logging.info(f"User {message.from_user.id} started the bot")
    welcome_text = "Привет! Выбирай категорию анекдота:"
    await message.answer(welcome_text, reply_markup=keyboard)

# Обработчик нажатия кнопок
@dp.message(lambda message: message.text in buttons)
async def send_joke(message: types.Message):
    try:
        logging.info(f"User {message.from_user.id} requested a joke from category: {message.text}")
        joke = get_joke(message.text)
        if joke:
            await message.answer(joke)
        else:
            await message.answer("Извините, анекдот не найден 😔")
            logging.warning(f"No joke found for category: {message.text}")
    except Exception as e:
        logging.error(f"Error sending joke: {e}")
        await message.answer("Произошла ошибка при обработке запроса 😔")

# Quart веб-сервер
app = Quart(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    try:
        logging.info("Received a webhook update")
        update = types.Update.model_validate(await request.json)
        await dp.feed_update(bot, update)
        return "OK", 200
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return "Internal Server Error", 500

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старый вебхук
    try:
        await bot.set_webhook(WEBHOOK_URL)  # Устанавливаем новый
        logging.info(f"Вебхук установлен: {WEBHOOK_URL}")
        await app.run_task(host="0.0.0.0", port=8080)  # Запускаем Quart
    except Exception as e:
        logging.error(f"Ошибка при установке вебхука: {e}")
    finally:
        await bot.session.close()  # Закрываем сессию бота

if __name__ == "__main__":
    asyncio.run(main())