from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text='🧮Калькулятор',callback_data='calculator')],
    [InlineKeyboardButton(text='🎨Цвет дерева',callback_data='color_wood')],
    [InlineKeyboardButton(text='🪚Посмотреть проекты',callback_data='examples_order')],
    [InlineKeyboardButton(text='📩Обратная связь',url='tg://user?id=6329071300')],
    [InlineKeyboardButton(text='🔎Помощь',callback_data='help')]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🍃Меню',callback_data='menu')]])
