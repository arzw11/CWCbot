from aiogram import Router,F
from aiogram.types import CallbackQuery,InputMediaPhoto
from keyboards.pagination_kb import paginator_color,paginator_review,Pagination
from funcs.data_func import CWCorders,CWCdata,CWCcolors

router = Router()
@router.callback_query(F.data == 'color_wood')
async def cmd_color_wood(clbck:CallbackQuery):
    color_photo1 = CWCcolors('color_wood',1,'color')
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=color_photo1.get_color_wood(),
        reply_markup=paginator_color()
                               )
@router.callback_query(Pagination.filter(F.action.in_(['prev_color','next_color','-'])))
async def pag_color_handler(clbck:CallbackQuery, callback_data:Pagination):
    data = CWCdata('color_wood')
    pages_count = len(data.get_data())
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 2 else pages_count
    if callback_data.action == 'next_color':
        page = page_num + 1 if page_num < pages_count else 1
    color_photos=CWCcolors('color_wood',page,'color')
    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media=InputMediaPhoto(
            media=color_photos.get_color_wood()
        ),
        reply_markup=paginator_color(page)
    )

@router.callback_query(F.data == 'examples_order')
async def cmd_review(clbck:CallbackQuery):
    mediafile1 = CWCorders('prev_orders',1,'photo','name','material','cover','color')
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=mediafile1.get_photo_prev_orders(),
        caption=mediafile1.get_caption_prev_orders(),
        reply_markup=paginator_review()
    )

@router.callback_query(Pagination.filter(F.action.in_(['prev_review','next_review','_'])))
async def pag_review_handler(clbck: CallbackQuery, callback_data:Pagination):
    data = CWCdata('prev_orders')
    pages_count = len(data.get_data())
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 2 else pages_count
    if callback_data.action == 'next_review':
        page = page_num + 1 if page_num < pages_count else 1
    mediafile = CWCorders('prev_orders', page, 'photo', 'name', 'material', 'cover', 'color')
    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media= InputMediaPhoto(
            media=mediafile.get_photo_prev_orders(),
            caption=mediafile.get_caption_prev_orders()),
        reply_markup=paginator_review(page)
    )