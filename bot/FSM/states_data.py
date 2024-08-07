from aiogram.fsm.state import State, StatesGroup

class CalculatorFillForm(StatesGroup):
    fill_number = State()
    fill_name = State()
    fill_product = State()
    fill_length = State()
    fill_width = State()
    fill_depth = State()
    fill_underframe = State()
    fill_request = State()

class AddProject(StatesGroup):
    name = State()
    material = State()
    cover = State()
    color= State()
    image = State()

    current_project = None

    texts = {
        'AddProject:name': 'Введите название публикации заново:',
        'AddProject:material': 'Введите материал изделия заново:',
        'AddProject:cover': 'Введите покрытие изделия заново:',
        'AddProject:color': 'Введите цвет изделия заново:',
        'AddProject:image': 'Отправьте изображение изделия заново:',
    }

class AddColors(StatesGroup):
    image = State()

    current_color = None

class ChangePriceMaterial(StatesGroup):
    id = State()
    price = State()

class AddUnderframe(StatesGroup):
    name = State()
    price = State()

    current_underframe = None

    texts = {
        'AddUnderframe:name': 'Введите название подстолья заново:',
        'AddUnderframe:material': 'Введите цену подстолья заново:',
    }

class AddUtils(StatesGroup):
    id = State()
    image = State()
