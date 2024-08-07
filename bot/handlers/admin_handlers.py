from aiogram import Router,F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import AsyncOrm
from bot.FSM.states_data import AddProject, AddColors, ChangePriceMaterial, AddUnderframe, AddUtils
from bot.keyboards.kb import KeyboardsBuilder
from bot.utils.admin import IsAdmin
from bot.wordbook import text


router = Router()

admin_kb = KeyboardsBuilder(
    btns={
        '🎨Цвет дерева': 'colors',
        '🪚Проекты': 'projects',
        '🧮Калькулятор': 'calc_settings',
        '🖇Утилиты': 'utils',
        '🍃Меню': 'menu'
        },
    sizes=(1,)).get_inline_keyborad()


@router.message(Command('cwc'))
async def cmd_admin(message: Message, state: FSMContext):
    if IsAdmin().check_user(tg_id=message.from_user.id):
        await message.answer(**text.admin_text.as_kwargs(), reply_markup=admin_kb)
        await state.clear()

@router.callback_query(F.data == 'admin')
async def admin(clbck: CallbackQuery, state: FSMContext):
    if IsAdmin().check_user(tg_id=clbck.from_user.id):
        await clbck.message.answer(**text.admin_text.as_kwargs(), reply_markup=admin_kb)
        await state.clear()

@router.message(StateFilter('*'), Command('cancel_action'))
@router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    if AddProject.current_project:
        AddProject.current_project = None
    
    if AddColors.current_color:
        AddColors.current_color = None
    
    await state.clear()
    await message.answer('♦️Действия отменены.')

#########################################################################################
##################################Colors#################################################
#########################################################################################


@router.callback_query(F.data == 'colors')
async def cmd_colors(clbck: CallbackQuery):
    await clbck.message.answer(**text.admin_colors.as_kwargs(), reply_markup=KeyboardsBuilder(
                                   btns={'➕Добавить запись': 'add_color',
                                         '👀Показать записи': 'show_colors',
                                         '👨‍🔧Админ-панель': 'admin'},
                                    sizes=(2,1,)).get_inline_keyborad())

@router.callback_query(F.data == 'show_colors')
async def cmd_show_colors(clbck: CallbackQuery, session: AsyncSession):
    colors = await AsyncOrm.get_all_colors(session=session)
    if colors:
        for color in colors:
            await clbck.message.answer_photo(
                photo=color.image,
                reply_markup=KeyboardsBuilder(
                    btns={
                        '🙃Изменить': f'change_color_{color.id}',
                        '🥺Удалить': f'delete_color_{color.id}',
                    },
                    sizes=(2,)
                    ).get_inline_keyborad()
            )
    else:
        await clbck.message.answer(text='🧐Записей нет.')

@router.callback_query(F.data.startswith("delete_color_"))
async def delete_color(clbck: CallbackQuery, session: AsyncSession):
    color_id = clbck.data.split('_')[-1]
    await AsyncOrm.delete_color(session=session, color_id=color_id)

    await clbck.message.answer(text='❌Запись удалена.')

@router.callback_query(StateFilter(None), F.data.startswith('change_color_'))
async def change_color(
    clbck: CallbackQuery, state: FSMContext, session: AsyncSession
):
    color_id = clbck.data.split("_")[-1]

    current_color = await AsyncOrm.get_color(session=session, color_id=color_id)

    AddColors.current_color = current_color

    await clbck.message.answer(text="Отправьте изображение.")
    await state.set_state(AddColors.image)

@router.callback_query(F.data == 'add_color')
async def add_color(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text="Отправьте изображение.")
    await state.set_state(AddColors.image)


@router.message(AddColors.image, F.photo)
async def get_color_image(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)

    data = await state.get_data()

    try:
        if AddColors.current_color:
            await AsyncOrm.change_color(session=session, color_id=AddColors.current_color.id, data=data)
            await message.answer(text='😵‍💫Запись изменена.',)
            
            await state.clear()
        else:
            await AsyncOrm.add_color(session=session, data=data)
            await message.answer(text='✅Запись была добавлена.')

            await state.clear()
    except Exception as e:
        await message.answer(text=f'❗️❗️❗️\n\nОшибка: {e}\n\nОбратитесь к создателю.')
        await state.clear()
    
    AddColors.current_color = None


#########################################################################################
##################################Projects###############################################
#########################################################################################


@router.callback_query(F.data == 'projects')
async def cmd_projects(clbck: CallbackQuery):
    await clbck.message.answer(**text.admin_project.as_kwargs(), 
                               reply_markup=KeyboardsBuilder(
                                   btns={'➕Добавить запись': 'add_project',
                                         '👀Показать записи': 'show_projects',
                                         '👨‍🔧Админ-панель': 'admin'},
                                    sizes=(2,1,)).get_inline_keyborad())

@router.callback_query(F.data == 'show_projects')
async def show_projects(clbck: CallbackQuery, session: AsyncSession):
    projects = await AsyncOrm.get_all_projects(session=session)
    if projects:
        for project in projects:
            await clbck.message.answer_photo(
                photo=project.image,
                caption=f"{project.name}\n\n▪Столешница: {project.material}\n▪Покрытие: {project.cover}\n▪Цвет: {project.color}\n\n📷Фотографии заказчика.",
                reply_markup=KeyboardsBuilder(
                    btns={
                        '🙃Изменить': f'change_project_{project.id}',
                        '🥺Удалить': f'delete_project_{project.id}',
                    },
                    sizes=(2,)
                    ).get_inline_keyborad()
            )
    else:
        await clbck.message.answer(text='🧐Записей нет.')

@router.callback_query(F.data.startswith("delete_project_"))
async def delete_project(clbck: CallbackQuery, session: AsyncSession):
    project_id = clbck.data.split('_')[-1]
    await AsyncOrm.delete_project(session=session, project_id=project_id)

    await clbck.message.answer(text='❌Запись удалена.')

@router.callback_query(F.data == 'add_project')
async def add_project(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(AddProject.name)
    await clbck.message.answer(text='Введите название публикации.')

@router.message(StateFilter('*'), Command('back_step_project'))
@router.message(StateFilter('*'), F.text.casefold() == "вернуться")
async def back_step(message: Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProject.name:
        await message.answer('Введите название публикации или напишите "отмена".')
        return

    previous = None
    for step in AddProject.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу.\n{AddProject.texts[previous.state]}")
            return
        previous = step

@router.callback_query(StateFilter(None), F.data.startswith("change_project_"))
async def change_project(clbck: CallbackQuery, state: FSMContext, session: AsyncSession):
    project_id = clbck.data.split("_")[-1]

    current_project = await AsyncOrm.get_project(session=session, project_id=project_id)

    AddProject.current_project = current_project

    await clbck.message.answer(text="Введите название публикации.")
    await state.set_state(AddProject.name)

@router.message(AddProject.name, F.text)
async def get_project_name(message: Message, state: FSMContext):
    if message.text == '.' and AddProject.current_project:
        await state.update_data(name=AddProject.current_project.name)
    else:    
        await state.update_data(name=message.text)
    await message.answer(text='Введите материал изделия.')
    await state.set_state(AddProject.material)

@router.message(AddProject.material, F.text)
async def get_project_material(message: Message, state: FSMContext):
    if message.text == '.' and AddProject.current_project:
        await state.update_data(material=AddProject.current_project.material)

    else:
        await state.update_data(material=message.text)

    await message.answer(text='Введите покрытие изделия.')
    await state.set_state(AddProject.cover)

@router.message(AddProject.cover, F.text)
async def get_project_cover(message: Message, state: FSMContext):
    if message.text == '.' and AddProject.current_project:
        await state.update_data(cover=AddProject.current_project.cover)
    else:
        await state.update_data(cover=message.text)

    await message.answer(text='Введите цвет изделия.')
    await state.set_state(AddProject.color)

@router.message(AddProject.color, F.text)
async def get_project_color(message: Message, state: FSMContext):
    if message.text == '.' and AddProject.current_project:
        await state.update_data(color=AddProject.current_project.color)

    else:
        await state.update_data(color=message.text)

    await message.answer(text='Отправьте изображение изделия.')
    await state.set_state(AddProject.image)

@router.message(AddProject.image, or_f(F.photo, F.text == '.'))
async def get_project_image(message: Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == '.' and AddProject.current_project:
        await state.update_data(image=AddProject.current_project.image)

    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)

    else:
        await message.answer(text='Отправьте изображение.')

    data = await state.get_data()

    try:
        if AddProject.current_project:
            await AsyncOrm.change_project(session=session,project_id=AddProject.current_project.id, data=data)
            await message.answer(text='😵‍💫Запись изменена.',)
            
            await state.clear()
        else:
            await AsyncOrm.add_project(session=session, data=data)
            await message.answer(text='✅Запись была добавлена.')

            await state.clear()
    except Exception as e:
        await message.answer(text=f'❗️❗️❗️\n\nОшибка: {e}\n\nОбратитесь к создателю.')
        await state.clear()
    
    AddProject.current_project = None


#########################################################################################
##################################Calculator#############################################
#########################################################################################

##################################Materials##############################################


@router.callback_query(F.data == 'calc_settings')
async def cmd_calc_settings(clbck: CallbackQuery):
    await clbck.message.answer(**text.admin_calculator.as_kwargs(),
                               reply_markup=KeyboardsBuilder(
                                   btns={
                                       '⚰️Материалы':'get_materials',
                                       '🦿Подстолья':'underframes',
                                       '👨‍🔧Админ-панель':'admin',
                                   },
                                   sizes=(2,1,)
                               ).get_inline_keyborad()
    )
    await clbck.answer()

@router.callback_query(F.data == 'get_materials')
async def materials(clbck: CallbackQuery, state: FSMContext, session=AsyncSession):
    materials = await AsyncOrm.get_all_materials(session=session)
    if materials:
        btns = {}

        for material in materials:
            btns[material.name] = f'change_material_{material.id}'
        
        btns['Админ-панель'] = 'admin'
        await clbck.message.answer(**text.admin_material.as_kwargs(),
                                reply_markup=KeyboardsBuilder(
                                    btns=btns,
                                    sizes=(2,)
                                ).get_inline_keyborad())
        
        await state.set_state(ChangePriceMaterial.id)
        
    else:
        await clbck.message.answer(text='🧐Записей нет.')


@router.callback_query(ChangePriceMaterial.id, F.data.startswith("change_material_"))
async def get_material_id(clbck: CallbackQuery, state: FSMContext):
    material_id = clbck.data.split('_')[-1]
    await state.update_data(id=material_id)

    await clbck.message.answer(text='Введите цену материала.')
    await state.set_state(ChangePriceMaterial.price)

@router.message(ChangePriceMaterial.price, F.text)
async def get_material_price(message: Message, state: FSMContext, session: AsyncSession):
    price = [i for i in message.text]
    result = all(map(lambda x: True if x.isdigit() else False, price))

    if result:
        await state.update_data(price=int(message.text))
        data = await state.get_data()

        try:
            await AsyncOrm.change_material_price(session=session, data=data)
            await message.answer(text='😵‍💫Запись изменена.')

            await state.clear()

        except Exception as e:
            await message.answer(text=f'❗️❗️❗️\n\nОшибка: {e}\n\nОбратитесь к создателю.')
            await state.clear()
    
    else:
        await message.answer(text='Введите цену материала.')


##################################Underframe#############################################

@router.callback_query(F.data == 'underframes')
async def cmd_underframe(clbck: CallbackQuery):
    await clbck.message.answer(**text.admin_underframe.as_kwargs(),
                               reply_markup=KeyboardsBuilder(
                                   btns={
                                       '➕Добавить запись': 'add_underframe',
                                       '👀Показать записи': 'show_underframes',
                                       '👨‍🔧Админ-панель': 'admin',
                                   },
                                   sizes=(2,)
                               ).get_inline_keyborad())



@router.callback_query(F.data == 'show_underframes')
async def show_underframe(clbck: CallbackQuery, session: AsyncSession):
    underframes = await AsyncOrm.get_all_underframes(session=session)
    if underframes:
        for underframe in underframes:
            await clbck.message.answer(text=f'🦿{underframe.name}\n\n💵{underframe.price} ₽.',
                reply_markup=KeyboardsBuilder(
                    btns={
                        '🙃Изменить': f'change_underframe_{underframe.id}',
                        '🥺Удалить': f'delete_underframe_{underframe.id}',
                    },
                    sizes=(2,)
                    ).get_inline_keyborad()
            )
    else:
        await clbck.message.answer(text='🧐Записей нет.')

@router.callback_query(F.data.startswith("delete_underframe_"))
async def delete_underframe(clbck: CallbackQuery, session: AsyncSession):
    underframe_id = clbck.data.split('_')[-1]
    await AsyncOrm.delete_underframe(session=session, underframe_id=underframe_id)

    await clbck.message.answer(text='❌Запись удалена.')



@router.callback_query(F.data == 'add_underframe')
async def add_underframe(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(AddUnderframe.name)
    await clbck.message.answer(text='Введите название подстолья.')

@router.message(StateFilter('*'), Command('back_step_underframe'))
@router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def back_step_underframe(message: Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddUnderframe.name:
        await message.answer('Введите название подстолья или напишите "отмена".')
        return

    previous = None
    for step in AddUnderframe.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу\n{AddUnderframe.texts[previous.state]}")
            return
        previous = step

@router.callback_query(StateFilter(None), F.data.startswith("change_underframe_"))
async def change_underframe(clbck: CallbackQuery, state: FSMContext, session: AsyncSession):
    underframe_id = clbck.data.split("_")[-1]

    current_underframe = await AsyncOrm.get_underframe(session=session, underframe_id=underframe_id)

    AddUnderframe.current_underframe = current_underframe

    await clbck.message.answer(text="Введите название подстолья.")
    await state.set_state(AddUnderframe.name)

@router.message(AddUnderframe.name, F.text)
async def get_underframe_name(message: Message, state: FSMContext):
    if message.text == '.' and AddUnderframe.current_underframe:
        await state.update_data(name=AddUnderframe.current_underframe.name)
    else:    
        await state.update_data(name=message.text)
    await message.answer(text='Введите цену подстолья.')
    await state.set_state(AddUnderframe.price)

@router.message(AddUnderframe.price, F.text)
async def get_underframe_price(message: Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == '.' and AddUnderframe.current_underframe:
        await state.update_data(price=AddUnderframe.current_underframe.price)

    else:
        await state.update_data(price=message.text)

    data = await state.get_data()

    try:
        if AddUnderframe.current_underframe:
            await AsyncOrm.change_underframe(session=session, underframe_id=AddUnderframe.current_underframe.id, data=data)
            await message.answer(text='😵‍💫Запись изменена.',)
            
            await state.clear()
        else:
            await AsyncOrm.add_underframe(session=session, data=data)
            await message.answer(text='✅Запись была добавлена.')

            await state.clear()
    except Exception as e:
        await message.answer(text=f'❗️❗️❗️\n\nОшибка: {e}\n\nОбратитесь к создателю.')
        await state.clear()
    
    AddUnderframe.current_underframe = None

#########################################################################################
##################################Utils#############################################
#########################################################################################

@router.callback_query(F.data == 'utils')
async def show_utils(clbck: CallbackQuery, state: FSMContext, session:AsyncSession):
    utils = await AsyncOrm.get_all_utils(session=session)
    if utils:
        btns = {}

        for util in utils:
            btns[f'🖇{util.name}'] = f'change_util_{util.id}'

        btns['👨‍🔧Админ-панель'] = 'admin'

        utils_kb = KeyboardsBuilder(
            btns=btns,
            sizes=(2,)
        ).get_inline_keyborad()

        await clbck.message.answer(**text.admin_utils.as_kwargs(), reply_markup=utils_kb)
        await state.set_state(AddUtils.id)
    else:
        await clbck.message.answer(text='🧐Записей нет.')


@router.callback_query(AddUtils.id, F.data.startswith('change_util_'))
async def get_util_id(clbck: CallbackQuery, state: FSMContext):
    util_id = clbck.data.split('_')[-1]
    await state.update_data(id=util_id)

    await clbck.message.answer(text='Отправьте изображение.')
    await state.set_state(AddUtils.image)

@router.message(AddUtils.image, F.photo)
async def get_util_photo(message: Message, state: FSMContext, session: AsyncSession):
    if message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        data = await state.get_data()
        try:
            await AsyncOrm.change_util(session=session, util_id=data['id'], data=data)
            await message.answer(text='😵‍💫Запись изменена.')

            await state.clear()

        except Exception as e:
            await message.answer(text=f'❗️❗️❗️\n\nОшибка: {e}\n\nОбратитесь к создателю.')
            await state.clear()
    else:
        message.answer(text='Отправьте изображение.')