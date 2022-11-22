from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    last_attempt = KeyboardButton(text='Получить предыдущий запрос')
    help_button = KeyboardButton(text='Справка')
    description_button = KeyboardButton(text='Описание')
    search_button = KeyboardButton(text='Выбрать ресурс для поиска')
    keyboard.add(last_attempt).add(description_button, help_button).add(search_button)
    return keyboard


def resource_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='МВидео', callback_data='res_mvideo')],
        [InlineKeyboardButton(text='СберМаркет', callback_data='res_sbermarket')],
        [InlineKeyboardButton(text='DNS', callback_data='res_dns')],
        [InlineKeyboardButton(text='Корпорация Центр', callback_data='res_kcent')],
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
    ])
    return keyboard
