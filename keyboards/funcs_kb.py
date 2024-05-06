from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

depth = [
    [InlineKeyboardButton(text='18 мм',callback_data='small_depth')],
    [InlineKeyboardButton(text='40 мм',callback_data='big_depth')]
]

depth = InlineKeyboardMarkup(inline_keyboard=depth)

def underframes_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Для барной стойки',callback_data='bar'),
        InlineKeyboardButton(text='Трапеция', callback_data='trapeze'),
        InlineKeyboardButton(text='Подстолье Х', callback_data='x'),
        InlineKeyboardButton(text='Подстолье Х-2', callback_data='x_two'),
        InlineKeyboardButton(text='Прямоугольное', callback_data='square'),
        InlineKeyboardButton(text='Подстолье "Гранд"', callback_data='grand'),
        InlineKeyboardButton(text='Подстолье "GEOMETRY"', callback_data='geometry'),
        InlineKeyboardButton(text='Подстолье обеденное', callback_data='dinner'),
        InlineKeyboardButton(text='Подстолье "MAXIMUM"', callback_data='maximum'),
        InlineKeyboardButton(text='Без подстолья',callback_data='none'),
        width=2
    )
    return builder.as_markup()

def order_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='🪑Стол',callback_data='table'),
        InlineKeyboardButton(text='💡Иное изделие', callback_data='other'),
        width=2
    )
    return builder.as_markup()

def bid_kb():
    builder =InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='📨Отправить',callback_data='send'),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=2
    )
    return builder.as_markup()


