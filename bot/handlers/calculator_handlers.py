from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import (TextLink,Italic,
    Bold, as_marked_section,as_list)

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import AsyncOrm
from bot.FSM.states_data import CalculatorFillForm
from bot.keyboards.kb import KeyboardsBuilder, exit_menu
from bot.utils.calculator import check_number, calculate_price
from bot.wordbook.text import (fill_form_text,choice_product,
    link_text, incorrect_number, get_number)

from config.config_reader import config

router = Router()

@router.callback_query(F.data == 'calculator')
async def cmd_calc(clbck:CallbackQuery,state: FSMContext):
    await state.set_state(CalculatorFillForm.fill_name)
    await state.update_data(fill_name = clbck.from_user.full_name)
    await state.set_state(CalculatorFillForm.fill_product)
    await clbck.message.answer(fill_form_text['product'],
                               reply_markup=KeyboardsBuilder(
        btns={
            '🪑Стол': 'table',
            '💡Иное изделие': 'other'
        },
        sizes=(2,)
    ).get_inline_keyborad())

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
        await message.answer(fill_form_text['depth'],reply_markup=KeyboardsBuilder(
            btns={
                '18 мм': 'depth_18',
                '40 мм': 'depth_40',
            },
            sizes=(2,)
        ).get_inline_keyborad())
    else:
        await message.answer(fill_form_text['incorrect'])
@router.callback_query(CalculatorFillForm.fill_depth, F.data.startswith('depth_'))
async def cmd_fill_depth(clbck: CallbackQuery, state: FSMContext, session: AsyncSession):
    underframes = await AsyncOrm.get_all_underframes(session=session)
    if underframes:
        btns = {}
        
        for underframe in underframes:
            btns[underframe.name] = f'underframe_{underframe.id}'
        
        btns['Без подстолья'] = 'underframe_0'

    kb = KeyboardsBuilder(
        btns=btns,
        sizes=(2,)
    ).get_inline_keyborad()    
        
    underframe_content = await AsyncOrm.get_util(session=session, util_id=1)
    depth = int(clbck.data.split('_')[-1])
    
    await state.update_data(fill_depth=depth)
    await state.set_state(CalculatorFillForm.fill_underframe)
    await clbck.bot.send_photo(
        chat_id= clbck.message.chat.id,
        photo= underframe_content.image,
        caption ='Выберите подстолье или пропустите этот шаг, нажав кнопку «Без подстолья».',
        reply_markup=kb
    )

@router.callback_query(CalculatorFillForm.fill_underframe,F.data.startswith('underframe_'))
async def cmd_fill_underframe(clbck: CallbackQuery, state: FSMContext, session: AsyncSession):
    underframe = clbck.data.split('_')[-1]
    await state.update_data(fill_underframe = underframe)
    await state.set_state(CalculatorFillForm.fill_number)
    data = await state.get_data()
    price_pine, price_larch = await calculate_price(data=data, session=session)
    if data['fill_underframe'] != '0':
        result = await AsyncOrm.get_underframe(session=session, underframe_id=data['fill_underframe'])
        underframe_name = result.name
    else:
        underframe_name = 'Без подстолья'

    caption = as_list(
        as_marked_section(
            Bold('CLEVER WOOD CONSTRUCTION'),
            f"Имя: {data['fill_name']}",
            f"Тип изделия: {data['fill_product']}",
            f"Длина: {data['fill_length']}см",
            f"Ширина: {data['fill_width']}см",
            f"Толщина: {data['fill_depth']}мм",
            f"Подстолье: {underframe_name}",
            marker='🪵'
                          ),
        as_marked_section(
            Italic('Указанная стоимость не является финальной ценой!'),
            f"Стол из сосны - {round(price_pine, 2)} ₽",
            f"Стола из лиственницы - {round(price_larch, 2)} ₽",
            marker='💵'
            ),
        as_marked_section(
            Bold('Для уточнения финальной стоимости, отправьте заявку, и наш специалист свяжется с вами для обсуждения деталей.'),
            'Отправить заявку?'
        ),
        sep='\n\n'
    )
    await clbck.message.answer(**caption.as_kwargs(),reply_markup=KeyboardsBuilder(
        btns={
            '📨Отправить': 'send',
            '🍃Меню': 'menu',
        },
        sizes=(2,)
    ).get_inline_keyborad())

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
    await message.answer(**content.as_kwargs(),reply_markup=KeyboardsBuilder(
        btns={
            '📨Отправить': 'send',
            '🍃Меню': 'menu',
        },
        sizes=(2,)
    ).get_inline_keyborad())

@router.callback_query(CalculatorFillForm.fill_number,F.data == 'send')
async def cmd_get_number(clbck:CallbackQuery,state:FSMContext):
    await clbck.message.answer(**get_number.as_kwargs())

@router.message(CalculatorFillForm.fill_number)
async def send_bid(message:Message,state:FSMContext, session: AsyncSession):
    if check_number(message.text) == True:
        await state.update_data(fill_number = message.text)
        data = await state.get_data()

        if data['fill_product'] == 'стол':
            if data['fill_underframe'] != '0':
                result = await AsyncOrm.get_underframe(session=session, underframe_id=data['fill_underframe'])
                underframe_name = result.name
            else:
                underframe_name = 'Без подстолья'
            price_pine, price_larch = await calculate_price(data=data, session=session)
            bid_content_table =as_list(
            as_marked_section(
                TextLink(f"ОТКРЫТЬ ЧАТ", url=f"https://t.me/+{data['fill_number']}"),
                f"Имя: {data['fill_name']}",
                f"Номер телефона: +{data['fill_number']}",
                f"Тип изделия: {data['fill_product']}",
                f"Длина: {data['fill_length']}см",
                f"Ширина: {data['fill_width']}см",
                f"Толщина: {data['fill_depth']}мм",
                f"Подстолье: {underframe_name}",
                marker='🪵'
                          ),
            as_marked_section(
                Italic('Примерная стоимость'),
                f"Стол из сосны - {round(price_pine, 2)} ₽",
                f"Стол из лиственницы - {round(price_larch, 2)} ₽",
                marker='💵'
                ),
            sep='\n\n'
            )
            await message.bot.send_message(chat_id=config.owner,**bid_content_table.as_kwargs())
            await message.bot.send_message(chat_id=config.cwc, **bid_content_table.as_kwargs())
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
            await message.bot.send_message(chat_id=config.owner,**bid_content.as_kwargs())
            await message.bot.send_message(chat_id=config.cwc, **bid_content.as_kwargs())
            await message.answer(**link_text.as_kwargs(),
                                       reply_markup=exit_menu
                                       )
            await state.clear()
    else:
        await message.answer(**incorrect_number.as_kwargs())
