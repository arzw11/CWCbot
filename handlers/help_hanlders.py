from aiogram import Router,F
from aiogram.types import CallbackQuery
from keyboards.help_kb import help_menu,back_help
from wordbook.text import help_text,help_bot_text,help_materials,help_consultation,help_social_network

router = Router()

@router.callback_query(F.data == 'help')
async def cmd_help(clbck:CallbackQuery):
    await clbck.message.answer(**help_text.as_kwargs(),reply_markup=help_menu)
@router.callback_query(F.data == 'funcs_bot')
async def cmd_help_funcs_bot(clbck:CallbackQuery):
    await clbck.message.answer(**help_bot_text.as_kwargs(),reply_markup=back_help())
@router.callback_query(F.data == 'materials')
async def cmd_help_materials(clbck:CallbackQuery):
    await clbck.message.answer(**help_materials.as_kwargs(),reply_markup=back_help())
@router.callback_query(F.data == 'consultation')
async def cmd_help_consultation(clbck:CallbackQuery):
    await clbck.message.answer(**help_consultation.as_kwargs(),reply_markup=back_help())
@router.callback_query(F.data == 'social_network')
async def cmd_help_social_network(clbck:CallbackQuery):
    await clbck.message.answer(**help_social_network.as_kwargs(),reply_markup=back_help())