from aiogram import Router,F
from aiogram.types import CallbackQuery,InputMediaPhoto
from keyboards.pagination_kb import paginator_color,paginator_review,Pagination
from funcs.data_func import get_data
from wordbook.text import review

router = Router()
@router.callback_query(F.data == 'color_wood')
async def cmd_color_wood(clbck:CallbackQuery):
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=get_data('color_wood')[0][0],
        reply_markup=paginator_color()
                               )
@router.callback_query(Pagination.filter(F.action.in_(['prev_color','next_color','-'])))
async def pag_color_handler(clbck:CallbackQuery, callback_data:Pagination):
    pages_count =len(get_data('color_wood'))
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else pages_count -1

    if callback_data.action == 'next_color':
        page = page_num + 1 if page_num < pages_count -1 else 0

    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media=InputMediaPhoto(
            media=get_data('color_wood')[page][0]
        ),
        reply_markup=paginator_color(page)
    )

@router.callback_query(F.data == 'examples_order')
async def cmd_review(clbck:CallbackQuery):
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=get_data('review')[0][0],
        caption=review[get_data('review')[0][1]],
        reply_markup=paginator_review()
    )

@router.callback_query(Pagination.filter(F.action.in_(['prev_review','next_review','_'])))
async def pag_review_handler(clbck: CallbackQuery, callback_data:Pagination):
    pages_count = len(get_data('review'))
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else pages_count-1

    if callback_data.action == 'next_review':
        page = page_num + 1 if page_num < pages_count-1 else 0
    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media= InputMediaPhoto(
            media=get_data('review')[page][0],
            caption= review[get_data('review')[page][1]]),
        reply_markup=paginator_review(page)
    )