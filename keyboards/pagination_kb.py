from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from funcs.data_func import CWCdata
class Pagination(CallbackData,prefix='pag'):
    action: str
    page: int

def paginator_review(page: int=1):
    orders_data = CWCdata('prev_orders')
    pages_count = len(orders_data.get_data())
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️',callback_data=Pagination(action='prev_review',page=page).pack()),
        InlineKeyboardButton(text=f"{str(page)}/{str(pages_count)}", callback_data='_'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_review', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()

def paginator_color(page: int=1):
    color_data = CWCdata('color_wood')
    pages_count = len(color_data.get_data())
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️',callback_data=Pagination(action='prev_color',page=page).pack()),
        InlineKeyboardButton(text=f'{str(page)}/{str(pages_count)}',callback_data='-'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_color', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()