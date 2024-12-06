from aiogram.utils.formatting import Text,Italic,Bold,as_list,as_marked_section,Spoiler,as_section,TextLink


start_text = as_list(
    Text('Добрый день!'),
    Text(Bold('Я бот компании CLEVER WOOD CONSTRUCTION — столярной мастерской в Красноярске с собственным производством.')),
    as_marked_section(
        Text('Изготовим для Вас:'),
        'столешницы из массива дерева',
        'компьютерный стол',
        'обеденный стол',
        'письменный стол',
        'журнальный столик'
        'полки',
        'стеллажи',
        'мебель из паллет',
        'и другое',
        marker='🪵'
    ),
    Text(
        'С помощью этого телеграм-бота Вы можете рассчитать стоимость интересующего изделия и оформить заявку для связи с руководством.'
    ),
    Text(Italic('Если Вы хотите узнать больше о возможностях бота, нажмите на кнопку «Помощь».')),
    sep='\n\n'
)
help_text = as_list(
    as_marked_section(
        Bold('''🌳CLEVER WOOD CONSTRUCTION🌳
        '''),
        'любые формы и рaзмеры',
        'cопpовождeниe покупателя от A до Я',
        'товар напрямую со склада без посредничества',
        'честная гарантия от производителя',
        'доставка + сборка',
        marker='🔥'
    ),
    Text(Spoiler(Italic('Единственный способ сделать выдающуюся работу – искренне любить то, что делаешь.')),Spoiler('© Стив Джобс')),
    Text(Bold('Выберите тему для получения помощи:')),
    sep='\n\n'
)
help_bot_text = as_list(
    as_marked_section(
        Bold('''🌳CLEVER WOOD CONSTRUCTION🌳
        '''),
        Text(Bold('«Калькулятор»'),' — наш бот поможет вам рассчитать примерную стоимость изделия. Также Вы сможете оставить заявку для связи с нами. Финальная цена обговаривается с представителями компании.'),
        Text(Bold('«Цвет дерева»'), ' — обзор доступных оттенков изделий.'),
        Text(Bold('«Посмотреть проекты»'),' — ознакомьтесь с нашими выполненными проектами.'),
        Text(Bold('«Обратная связь»'),' — наш чат.'),
        marker='🤖'
    )
)
help_materials = as_list(
    as_section(
        Bold('☝️ Пожалуйста, обратите внимание:'),
        'Мы не производим “одноразовые” столы из ДСП покрытые шпоном и прочих дешевых материалов! У нас используются только натуральные материалы, которые прослужат Вам и Вашим родным долгие годы.'
    ),
    as_marked_section(
        Bold('Всегда в наличии:'),
        'массив сосны',
        'массив лиственницы',
        'массив ясеня и др.',
        marker='🌵'
    ),
    Text(Italic('🪚 Подстолье на выбор: металлическое (белое или черное), деревянное.')),
    sep='\n\n'
)
help_consultation = as_list(
    Text('Вы можете связаться с нами через кнопку ',Bold('«Обратная связь»')),
    as_marked_section(
        Bold('Консультация на производстве:'),
        'Встреча на производстве по предварительному звонку.',
        marker='🕰'
    ),
    TextLink('📍Адрес цеха: г. Красноярск, ул. Полигонная, 8 ст. 7',url='https://2gis.ru/krasnoyarsk/geo/70000001083452196'),
    sep='\n\n'
)
help_social_network = as_list(
    Text(Bold('🌳CLEVER WOOD CONSTRUCTION🌳')),
    as_marked_section(
        'Мы в соцсетях:',
        TextLink('VK',url='https://vk.com/cwc_kras'),
        TextLink('INSTAGRAM',url='https://www.instagram.com/cwc_kras?igsh=MWVkajh6aWZhdzYxYQ=='),
        TextLink('AVITO',url='https://www.avito.ru/user/d150d3fef0d2425d1c9b4859783f04c5/profile/all?id=4082263893&src=item&page_from=from_item_card&iid=4082263893&sellerId=d150d3fef0d2425d1c9b4859783f04c5'),
        marker='🗺'
    ),
    Text('☎️ Мы всегда на связи и готовы предоставить Вам профессиональную консультацию.'),
    sep='\n\n'
)
get_number = as_list(
    as_marked_section(
        Bold('Для отправки заявки, вам необходимо указать номер телефона'),
        Text('Введите номер телефона в формате ',Bold('79876543210')),
        marker='📞'
    ),
    sep='\n\n'
)
incorrect_number = as_list(
    as_marked_section(
        Bold('Введенный вами номер указан не в том формате'),
        'Введите номер телефона в формате 79876543210',
        marker='📞'
    ),
    sep='\n\n'
)
fill_form_text = {
    'product': 'Выберите изделие.',
    'length': 'Укажите длину столешницы в сантиметрах.',
    'width': 'Отлично, теперь укажите ширину столешницы в сантиметрах.',
    'incorrect': 'Введите положительное число.',
    'depth': 'Укажите толщину столешницы в миллиметрах.',
    'request': 'Укажите, какое изделие вы хотите заказать.',
}
choice_product = {
    'table': 'стол',
    'other': 'иное изделие'
}
link_text = as_list(
    as_marked_section(
    Bold('Ваша заявка успешно отправлена!'),
    Italic('В течение дня с вами свяжется наш представитель'),
        marker='❗️'
    )
)
cancel_text = as_list(
    Text(Bold('Вы вернулись в главное меню.')),
    Text(Bold('🌳CLEVER WOOD CONSTRUCTION🌳')),
    as_marked_section(
        Text('Изготовим для Вас:'),
        'столешницы из массива дерева',
        'компьютерный стол',
        'обеденный стол',
        'письменный стол',
        'журнальный столик'
        'полки',
        'стеллажи',
        'мебель из паллет',
        'и другое',
        marker='🪵'
    ),
    Text(
        'С помощью этого телеграм-бота Вы можете рассчитать стоимость интересующего изделия и оформить заявку для связи с руководством.'
    ),
    Text(Italic('Если Вы хотите узнать больше о возможностях бота, нажмите на кнопку «Помощь».')),
    sep='\n\n'
)

admin_text = as_list(
    Text(Bold('👨‍🔧АДМИН-ПАНЕЛЬ CWC')),
    Text('Данная админ-панель поможет тебе редактировать записи в БД без вмешательства в код программы.'),
    as_marked_section(
        Text(Bold('Редактируемые категории:')),
        'Цвета дерева',
        'Проекты',
        'Калькулятор',
        'Утилиты',
        marker='🍁'
    ),
    TextLink('Обратная связь.',url='https://t.me/hopelesstard1'),
    sep='\n\n'
)

admin_colors = as_list(
    Text(Bold('🎨ЦВЕТ ДЕРЕВА')),
    Text('Ты можешь добавить, изменить и удалить изображения выкрасов дерева.'),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        marker='🪄'
    ),
    sep='\n\n'
)

admin_project = as_list(
    Text(Bold('🪚ПРОЕКТЫ')),
    Text('Ты можешь добавить, изменить и удалить отзывы.'),
    as_marked_section(
        Text(Bold('Шаблон:')),
        'Заголовок публикации. Название записи.',
        'Материал, из которого было сделано изделие.',
        'Покрытие, которое вы использовали при работе.',
        'Цвет дерева.',
        'Изображение. Только одна фотография(выбирай лучшую на твой взгляд.)',
        marker='📝'
    ),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '/back_step_project — вернуться на один шаг.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        '"Вернуться" — отправь в чат данное слово, чтобы вернуться на один шаг.',
        marker='🪄'
    ),
    sep='\n\n'
)

admin_calculator = as_list(
    Text(Bold('🧮НАСТРОЙКА КАЛЬКУЛЯТОРА')),
    Text('Ты можешь изменить цену материалов, а также добавить, изменить и удалить информацию о подстольях.'),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        marker='🪄'
    ),
    sep='\n\n'
)

admin_material = as_list(
    Text(Bold('⚰️МАТЕРИАЛЫ')),
    Text('Ты можешь изменить цену материалов.'),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        marker='🪄'
    ),
    sep='\n\n'
)

admin_underframe = as_list(
    Text(Bold('🦿ПОДСТОЛЬЯ')),
    Text('Ты можешь добавить, изменить и удалить информацию о подстольях.'),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '/back_step_underframe — вернуться на один шаг.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        '"Назад" — отправь в чат данное слово, чтобы вернуться на один шаг.',
        marker='🪄'
    ),
    sep='\n\n'
)

admin_utils = as_list(
    Text(Bold('🖇УТИЛИТЫ')),
    Text('Разного рода контент. В будущем при расширении функционала, может понадобиться. Сейчас можно изменить изображение подстолья.'),
    as_marked_section(
        Text(Bold('Полезные команды:')),
        '/cancel_action — отмена действия.',
        '"Отмена" — отправь в чат данное слово для отмены действия.',
        marker='🪄'
    ),
    sep='\n\n'
)