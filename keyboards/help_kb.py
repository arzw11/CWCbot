from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

help_menu = [
    [InlineKeyboardButton(text='🤖Функционал бота',callback_data='funcs_bot')],
    [InlineKeyboardButton(text='⚒Материалы',callback_data='materials')],
    [InlineKeyboardButton(text='📝Консультация',callback_data='consultation')],
    [InlineKeyboardButton(text='🌐Социальные сети',callback_data='social_network')],
    [InlineKeyboardButton(text='🍃Меню',callback_data='menu')]
]

help_menu = InlineKeyboardMarkup(inline_keyboard=help_menu)

def back_help():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='🔙',callback_data='help'),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=2
    )
    return builder.as_markup()