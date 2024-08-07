from aiogram import Router,F
from aiogram.types import CallbackQuery,InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import AsyncOrm
from bot.keyboards.kb import Pagination, paginator_color, paginator_review

router = Router()


@router.callback_query(F.data == 'color_wood')
async def cmd_color_wood(clbck:CallbackQuery, session: AsyncSession):
    data = await AsyncOrm.get_all_colors(session=session)
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=data[0].image,
        reply_markup= await paginator_color(session=session)
                               )
@router.callback_query(Pagination.filter(F.action.in_(['prev_color','next_color','-'])))
async def pag_color_handler(clbck:CallbackQuery, callback_data:Pagination, session: AsyncSession):
    data = await AsyncOrm.get_all_colors(session=session)
    pages_count = len(data)
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else pages_count-1
    if callback_data.action == 'next_color':
        page = page_num + 1 if page_num < pages_count-1 else 0
    color = data[page]
    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media=InputMediaPhoto(
            media=color.image
        ),
        reply_markup= await paginator_color(session=session, page=page)
    )

@router.callback_query(F.data == 'examples_order')
async def cmd_review(clbck:CallbackQuery, session: AsyncSession):
    data = await AsyncOrm.get_all_projects(session=session)
    await clbck.bot.send_photo(
        chat_id=clbck.message.chat.id,
        photo=data[0].image,
        caption=f"{data[0].name}\n\n▪Столешница: {data[0].material}\n▪Покрытие: {data[0].cover}\n▪Цвет: {data[0].color}\n\n📷Фотографии заказчика.",
        reply_markup= await paginator_review(session=session)
    )

@router.callback_query(Pagination.filter(F.action.in_(['prev_review','next_review','_'])))
async def pag_review_handler(clbck: CallbackQuery, callback_data:Pagination, session: AsyncSession):
    data = await AsyncOrm.get_all_projects(session=session)
    pages_count = len(data)
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else pages_count-1
    if callback_data.action == 'next_review':
        page = page_num + 1 if page_num < pages_count-1 else 0
    rev = data[page]
    await clbck.bot.edit_message_media(
        chat_id=clbck.message.chat.id,
        message_id=clbck.message.message_id,
        media= InputMediaPhoto(
            media=rev.image,
            caption=f"{rev.name}\n\n▪Столешница: {rev.material}\n▪Покрытие: {rev.cover}\n▪Цвет: {rev.color}\n\n📷Фотографии заказчика."),
        reply_markup= await paginator_review(session=session, page=page)
    )