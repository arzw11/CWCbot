from aiogram import Router,F
from aiogram.filters.command import Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text,Bold
from keyboards import menu_kb
from wordbook.text import start_text,cancel_text

router = Router()

@router.message(Command('start'))
async def cmd_start(message:Message):
    await message.answer(**start_text.as_kwargs(),reply_markup=menu_kb.menu)
@router.callback_query(F.data == 'menu')
async def cmd_back_menu(clbck:CallbackQuery, state:FSMContext):
    await state.clear()
    await clbck.message.answer(**cancel_text.as_kwargs(),reply_markup=menu_kb.menu)
@router.message(Command('cancel'))
async def cmd_cancel(message:Message,state:FSMContext):
    await state.clear()
    await message.answer(**cancel_text.as_kwargs(),reply_markup=menu_kb.menu)


