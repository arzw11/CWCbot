from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import AsyncOrm



class KeyboardsBuilder:
    def __init__(self, btns, sizes, placeholder=None):
        self.btns: dict[str, str] = btns
        self.sizes: tuple[int] = sizes
        self.placeholder: str = placeholder

    def get_inline_keyborad(self):
        builder = InlineKeyboardBuilder()

        for text, data in self.btns.items():
            builder.add(InlineKeyboardButton(text=text, callback_data=data))
        
        return builder.adjust(*self.sizes).as_markup()

    def get_reply_keyboard(self, start=0):
        builder = ReplyKeyboardBuilder()

        for text, index in self.btns.items():
            builder.add(KeyboardButton(text=text))

        return builder.adjust(*self.sizes).as_markup()


menu = [
    [InlineKeyboardButton(text='🧮Калькулятор',callback_data='calculator')],
    [InlineKeyboardButton(text='🎨Цвет дерева',callback_data='color_wood')],
    [InlineKeyboardButton(text='🪚Посмотреть проекты',callback_data='examples_order')],
    [InlineKeyboardButton(text='📩Обратная связь',url='tg://user?id=6329071300')],
    [InlineKeyboardButton(text='🔎Помощь',callback_data='help')]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🍃Меню',callback_data='menu')]])

class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int

async def paginator_review(session: AsyncSession, page: int=0):
    orders_data = await AsyncOrm.get_all_projects(session=session)
    pages_count = len(orders_data)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️', callback_data=Pagination(action='prev_review', page=page).pack()),
        InlineKeyboardButton(text=f"{str(page+1)}/{str(pages_count)}", callback_data='_'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_review', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()

async def paginator_color(session: AsyncSession, page: int=0):
    color_data = await AsyncOrm.get_all_colors(session=session)
    pages_count = len(color_data)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='↪️',callback_data=Pagination(action='prev_color',page=page).pack()),
        InlineKeyboardButton(text=f'{str(page+1)}/{str(pages_count)}',callback_data='-'),
        InlineKeyboardButton(text='↩️', callback_data=Pagination(action='next_color', page=page).pack()),
        InlineKeyboardButton(text='🍃Меню',callback_data='menu'),
        width=3
    )
    return builder.as_markup()