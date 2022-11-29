import json
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hlink
from aiogram.types import ReplyKeyboardRemove

from keyboards import main_menu_keyboard, resource_keyboard

from dotenv import load_dotenv

from resources.sbermarket.sbermarket import get_data_sbermarket
from resources.dns.dns import get_data_dns

load_dotenv()

TOKEN = str(os.environ.get('TOKEN'))

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('BOT STARTED')


class Form(StatesGroup):
    resource = State()
    search = State()
    page = State()


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    await message.answer(f'<b>Добро пожаловать!</b>\nЭтот бот позволит найти интересующее Вас товары на СберМаркете со скидкой!',
                         reply_markup=main_menu_keyboard())
    await message.delete()


@dp.message_handler(Text(equals='Выбрать ресурс для поиска'))
async def resource_command(message: types.Message):
    await message.answer(text='Вы перешли в меню выбора сайта!', reply_markup=ReplyKeyboardRemove())
    await message.answer(text='Пожалуйста выберете сайт для поиска!', reply_markup=resource_keyboard())
    await message.delete()


@dp.callback_query_handler(lambda x: x.data == 'main_menu')
async def get_main_menu(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, 'Возврат в главное меню!', reply_markup=main_menu_keyboard())


@dp.callback_query_handler(lambda x: x.data.startswith('res'))
async def get_resource(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['resource'] = callback.data.split('_')[-1]
    await Form.next()
    await Form.search.set()
    await callback.message.reply('Введите поисковый запрос:')


@dp.message_handler(state=Form.search)
async def get_discount_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search'] = message.text.strip()
        resource = data['resource']
    await message.answer('Идет поиск. Примерное время ожидания: 30 секунд\nОжидайте...')
    if resource == 'dns':
        get_data_dns(message.text, message.from_user.id)
    elif resource == 'sbermarket':
        get_data_sbermarket(message.text, message.from_user.id)
    with open(f'data/{resource}-{message.from_user["id"]}.json', encoding='utf-8') as file:
        data = json.load(file)
    for item in data[10]:
        item_name = item.get("item_name")
        item_price = item.get("item_price")
        item_url = item.get("item_url")
        item_discount = item.get("item_discount")
        item_old_price = item.get("item_old_price")
        card = f'{hlink(item_name, item_url)}\n' \
               f'{hbold("Цена:")} {item_price} ₽\n'
        if item_discount and item_old_price:
            card += f'{hbold("Скидка:")} -{item_discount}% (Старая цена: {item_old_price} ₽)'
        await message.answer(card)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Поиск завершен!', reply_markup=main_menu_keyboard())


def main():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
