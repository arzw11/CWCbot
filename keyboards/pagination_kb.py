from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from funcs.data_func import get_data
class Pagination(CallbackData,prefix='pag'):
    action: str
    page: int

def paginator_review(page: int=0):
    pages_count = len(get_data('review'))
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️',callback_data=Pagination(action='prev_review',page=page).pack()),
        InlineKeyboardButton(text=f"{str(page+1)}/{str(pages_count)}", callback_data='_'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_review', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()

def paginator_color(page: int=0):
    pages_count = len(get_data('color_wood'))
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️',callback_data=Pagination(action='prev_color',page=page).pack()),
        InlineKeyboardButton(text=f'{str(page+1)}/{str(pages_count)}',callback_data='-'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_color', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()