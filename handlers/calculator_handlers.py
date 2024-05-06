from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from aiogram.fsm.context import FSMContext
from FSM.states_data import CalculatorFillForm
from aiogram.utils.formatting import (TextLink,Italic,
    Bold, as_marked_section,as_list)
from keyboards.funcs_kb import order_kb,underframes_kb,bid_kb,depth
from keyboards.menu_kb import exit_menu
from funcs.calculator import calculation,check_number
from funcs.data_func import get_data
from wordbook.text import (fill_form_text,choice_product,
    link_text,underframe_price,incorrect_number,get_number)
from config_reader import config

router = Router()

@router.callback_query(F.data == 'calculator')
async def cmd_calc(clbck:CallbackQuery,state: FSMContext):
    await state.set_state(CalculatorFillForm.fill_name)
    await state.update_data(fill_name = clbck.from_user.full_name)
    await state.set_state(CalculatorFillForm.fill_product)
    await clbck.message.answer(fill_form_text['product'],reply_markup=order_kb())

@router.callback_query(CalculatorFillForm.fill_product,F.data=='table')
async def cmd_fill_product(clbck:CallbackQuery,state: FSMContext):
    await state.update_data(fill_product = choice_product[clbck.data])
    await state.set_state(CalculatorFillForm.fill_length)
    await clbck.message.answer(fill_form_text['length'])

@router.message(CalculatorFillForm.fill_length)
async def cmd_fill_length(message: Message,state: FSMContext):
    if message.text.isdigit() and int(message.text) > 0:
        await state.update_data(fill_length = int(message.text))
        await state.set_state(CalculatorFillForm.fill_width)
        await message.answer(fill_form_text['width'])
    else:
        await message.answer(fill_form_text['uncorrect'])
@router.message(CalculatorFillForm.fill_width)
async def cmd_fill_width(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) > 0:
        await state.update_data(fill_width = int(message.text))
        await state.set_state(CalculatorFillForm.fill_depth)
        await message.answer(fill_form_text['depth'],reply_markup=depth)
    else:
        await message.answer(fill_form_text['incorrect'])
@router.callback_query(CalculatorFillForm.fill_depth, F.data.in_(['small_depth','big_depth']))
async def cmd_fill_depth(clbck: CallbackQuery, state: FSMContext):
    if clbck.data == 'small_depth':
        await state.update_data(fill_depth=18)
        await state.set_state(CalculatorFillForm.fill_underframe)
        await clbck.bot.send_photo(
            chat_id= clbck.message.chat.id,
            photo=get_data('underframe')[0][0],
            caption=fill_form_text['underframe'],
            reply_markup=underframes_kb()
        )
    else:
        await state.update_data(fill_depth=40)
        await state.set_state(CalculatorFillForm.fill_underframe)
        await clbck.bot.send_photo(
            chat_id= clbck.message.chat.id,
            photo=get_data('underframe')[0][0],
            caption=fill_form_text['underframe'],
            reply_markup=underframes_kb()
        )
@router.callback_query(CalculatorFillForm.fill_underframe,
                       F.data.in_(['bar','trapeze','x','x_two','square','grand','geometry','dinner','maximum','none']))
async def cmd_fill_underframe(clbck: CallbackQuery, state: FSMContext):
    await state.update_data(fill_underframe = underframe_price[clbck.data])
    await state.set_state(CalculatorFillForm.fill_number)
    data = await state.get_data()
    price_pine,price_larch = calculation(data)
    caption = as_list(
        as_marked_section(
            Bold('CLEVER WOOD CONSTRUCTION'),
            f"Имя: {data['fill_name']}",
            f"Тип изделия: {data['fill_product']}",
            f"Длина: {data['fill_length']}см",
            f"Ширина: {data['fill_width']}см",
            f"Толщина: {data['fill_depth']}мм",
            f"Подстолье: {data['fill_underframe'][0]}",
            marker='🪵'
                          ),
        as_marked_section(
            Italic('Указанная стоимость не является финальной ценой!'),
            f"Стол из сосны - {price_pine}₽",
            f"Стола из лиственницы - {price_larch}₽",
            marker='💵'
            ),
        as_marked_section(
            Bold('Для уточнения финальной стоимости, отправьте заявку, и наш специалист свяжется с вами для обсуждения деталей.'),
            'Отправить заявку?'
        ),
        sep='\n\n'
    )
    await clbck.message.answer(**caption.as_kwargs(),reply_markup=bid_kb())
@router.callback_query(CalculatorFillForm.fill_product, F.data == 'other')
async def cmd_other(clbck: CallbackQuery,state:FSMContext):
    await state.update_data(fill_product = choice_product[clbck.data])
    await state.set_state(CalculatorFillForm.fill_request)
    await clbck.message.answer(fill_form_text['request'])
@router.message(CalculatorFillForm.fill_request)
async def cmd_fill_request(message:Message,state:FSMContext):
    await state.update_data(fill_request = message.text)
    await state.set_state(CalculatorFillForm.fill_number)
    data = await state.get_data()
    content = as_list(
        as_marked_section(
            Bold('CLEVER WOOD CONSTRUCTION'),
            f"Имя: {data['fill_name']}",
            f"Тип изделия: {data['fill_product']}",
            f"Комментарий - {data['fill_request']}",
            marker='🪵'
        ),
        as_marked_section(
            Bold('Для уточнения стоимости, отправьте заявку, и наш специалист свяжется с вами для обсуждения деталей.'),
            'Отправить заявку нашему представителю?'
        ),
        sep='\n\n'

    )
    await message.answer(**content.as_kwargs(),reply_markup=bid_kb())
@router.callback_query(CalculatorFillForm.fill_number,F.data == 'send')
async def cmd_get_number(clbck:CallbackQuery,state:FSMContext):
    await clbck.message.answer(**get_number.as_kwargs())
@router.message(CalculatorFillForm.fill_number)
async def send_bid(message:Message,state:FSMContext):
    if check_number(message.text) == True:
        await state.update_data(fill_number = message.text)
        data = await state.get_data()
        if data['fill_product'] == 'стол':
            price_pine, price_larch = calculation(data)
            bid_content_table =as_list(
            as_marked_section(
                TextLink(f"ОТКРЫТЬ ЧАТ", url=f"https://t.me/+{data['fill_number']}"),
                f"Имя: {data['fill_name']}",
                f"Номер телефона: +{data['fill_number']}",
                f"Тип изделия: {data['fill_product']}",
                f"Длина: {data['fill_length']}см",
                f"Ширина: {data['fill_width']}см",
                f"Толщина: {data['fill_depth']}мм",
                f"Подстолье: {data['fill_underframe'][0]}",
                marker='🪵'
                          ),
            as_marked_section(
                Italic('Примерная стоимость'),
                f"Стол из сосны - {price_pine}₽",
                f"Стол из лиственницы - {price_larch}₽",
                marker='💵'
                ),
            sep='\n\n'
            )
            await message.bot.send_message(chat_id=config.owner.get_secret_value(),**bid_content_table.as_kwargs())
            await message.bot.send_message(chat_id=config.cwc.get_secret_value(), **bid_content_table.as_kwargs())
            await message.answer(**link_text.as_kwargs(),
                                   reply_markup=exit_menu
                                   )
            await state.clear()
        else:
            bid_content = as_list(
                as_marked_section(
                TextLink('ОТКРЫТЬ ЧАТ', url=f"https://t.me/+{data['fill_number']}"),
                f"Имя:{data['fill_name']}",
                f"Номер телефона: +{data['fill_number']}",
                f"Тип изделия: {data['fill_product']}",
                f"Комментарий - {data['fill_request']}",
                marker='🪵'
                )
            )
            await message.bot.send_message(chat_id=owner,**bid_content.as_kwargs())
            await message.bot.send_message(chat_id=cwc, **bid_content.as_kwargs())
            await message.answer(**link_text.as_kwargs(),
                                       reply_markup=exit_menu
                                       )
            await state.clear()
    else:
        await message.answer(**incorrect_number.as_kwargs())