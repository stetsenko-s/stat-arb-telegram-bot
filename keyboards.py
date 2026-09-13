from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


about_button = InlineKeyboardButton(
    text='О проекте',
    callback_data='about'
)

pairs_button = InlineKeyboardButton(
    text='Подходящие пары',
    callback_data='pairs'
)

indicators_button = InlineKeyboardButton(
    text='О показателях',
    callback_data='indicators'
)

main_menu = InlineKeyboardButton(
    text='Главное меню',
    callback_data='main_menu'
)

back_to_pair = InlineKeyboardButton(
    text='Назад к списку',
    callback_data='pairs'
)

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [about_button, pairs_button, indicators_button]
    ]
)

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [main_menu]
    ]
)

pair_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [back_to_pair, main_menu]
    ]
)

def create_pairs_keyboard(pairs) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру выбора пары.

    Размещает каждую пару в отдельной строке и добавляет существующую
    кнопку main_menu. Передаёт идентификатор пары в формате pair:ID.
    Используется при показе списка; при пустом списке оставляет
    только кнопку главного меню.

    Args:
        pairs: list[dict] (содержит словари с полями symbol_1, symbol_2
                          и pair_id для формирования кнопок)

    Returns:
        InlineKeyboardMarkup: Новая клавиатура выбора пар и возврата.
    """
    arr = []
    for v in pairs:
        name = f'{v['symbol_1']} / {v['symbol_2']}'
        button = InlineKeyboardButton(text=name, callback_data=f'pair:{v['pair_id']}')
        arr.append([button])

    arr.append([main_menu])

    return InlineKeyboardMarkup(inline_keyboard=arr)


