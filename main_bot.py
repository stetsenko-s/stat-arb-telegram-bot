from gc import callbacks
from os import getenv

from aiogram.types import InlineKeyboardButton, Message
from aiogram.types import InlineKeyboardMarkup
from aiogram import F
from aiogram.types import CallbackQuery
from dotenv import load_dotenv

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


load_dotenv()
TOKEN = getenv('TOKEN')
dp = Dispatcher()


indicators_text = """
<b>О показателях</b>

<b>Спред</b>
Разность цен двух инструментов с учётом коэффициента их соотношения — hedge ratio.
Например: спред = цена A − hedge ratio × цена B.
Здесь речь о разнице между инструментами, а не между ценами покупки и продажи одного инструмента.

<b>Z-score</b>
Показывает, насколько текущий спред отклонился от своего среднего за выбранный период.
Значение +2 означает, что спред выше среднего на два стандартных отклонения, а −2 — ниже на столько же. Стандартное отклонение характеризует обычный разброс значений.
Большое отклонение само по себе не гарантирует возврат к среднему.

<b>P-value</b>
Показывает, насколько необычен результат теста при условии, что его исходная гипотеза верна.
Чем меньше p-value, тем больше оснований отвергнуть эту гипотезу. При пороге 0,05 результат считается статистически значимым, если p-value меньше 0,05.
Это не вероятность прибыльной сделки и не вероятность ошибочности гипотезы.

<b>Engle–Granger</b>
Тест на коинтеграцию: он помогает проверить, существует ли между ценами статистическая связь, при которой их определённая линейная комбинация остаётся стационарной.
Исходная гипотеза — коинтеграции нет. Малое p-value даёт основания её отвергнуть.
Связь, обнаруженная на исторических данных, может нарушиться в будущем.

<b>ADF-тест</b>
Проверяет наличие единичного корня — одного из признаков нестационарности временного ряда.
Исходная гипотеза — единичный корень есть. Малое p-value даёт основания отвергнуть её в пользу стационарности в рамках выбранной модели.
Для спреда стационарность означает, что его статистические свойства, например среднее и разброс, не меняются со временем. Это не означает, что его значение постоянно.

<b>Hedge ratio</b>
Коэффициент, который определяет вес второго инструмента при расчёте спреда.
Например, при значении 0,8 из цены A вычитается цена B, умноженная на 0,8.
Этот коэффициент оценивается по историческим данным и может меняться.

<b>Half-life</b>
Оценочное время, за которое ожидаемое отклонение спреда от равновесного уровня сокращается вдвое по используемой модели.
Например, 12 часов — оценка времени уменьшения отклонения наполовину, а не полного возврата к среднему.
В боте показатель отображается в часах; это оценка, а не точный срок.
""".strip()

pairs_data = [
    {
        "pair_id": "btc_eth",
        "symbol_1": "BTCUSDT",
        "symbol_2": "ETHUSDT",
        "z_score": 1.73,
        "eg_p_value": 0.0241,
    },
    {
        "pair_id": "sol_avax",
        "symbol_1": "SOLUSDT",
        "symbol_2": "AVAXUSDT",
        "z_score": -2.14,
        "eg_p_value": 0.0180,
    },
    {
        "pair_id": "bnb_eth",
        "symbol_1": "BNBUSDT",
        "symbol_2": "ETHUSDT",
        "z_score": 0.85,
        "eg_p_value": 0.0312,
    },
    {
        "pair_id": "ada_dot",
        "symbol_1": "ADAUSDT",
        "symbol_2": "DOTUSDT",
        "z_score": -1.62,
        "eg_p_value": 0.0125,
    },
    {
        "pair_id": "xrp_xlm",
        "symbol_1": "XRPUSDT",
        "symbol_2": "XLMUSDT",
        "z_score": 2.31,
        "eg_p_value": 0.0084,
    },
    {
        "pair_id": "doge_shib",
        "symbol_1": "DOGEUSDT",
        "symbol_2": "SHIBUSDT",
        "z_score": -0.47,
        "eg_p_value": 0.0421,
    },
    {
        "pair_id": "ltc_bch",
        "symbol_1": "LTCUSDT",
        "symbol_2": "BCHUSDT",
        "z_score": 1.95,
        "eg_p_value": 0.0193,
    },
    {
        "pair_id": "link_uni",
        "symbol_1": "LINKUSDT",
        "symbol_2": "UNIUSDT",
        "z_score": -2.56,
        "eg_p_value": 0.0057,
    },
    {
        "pair_id": "atom_dot",
        "symbol_1": "ATOMUSDT",
        "symbol_2": "DOTUSDT",
        "z_score": 0.12,
        "eg_p_value": 0.0376,
    },
    {
        "pair_id": "near_avax",
        "symbol_1": "NEARUSDT",
        "symbol_2": "AVAXUSDT",
        "z_score": -1.08,
        "eg_p_value": 0.0289,
    },
    {
        "pair_id": "arb_op",
        "symbol_1": "ARBUSDT",
        "symbol_2": "OPUSDT",
        "z_score": 2.04,
        "eg_p_value": 0.0142,
    },
    {
        "pair_id": "aave_comp",
        "symbol_1": "AAVEUSDT",
        "symbol_2": "COMPUSDT",
        "z_score": -1.89,
        "eg_p_value": 0.0217,
    },
    {
        "pair_id": "fil_ar",
        "symbol_1": "FILUSDT",
        "symbol_2": "ARUSDT",
        "z_score": 0.63,
        "eg_p_value": 0.0463,
    },
    {
        "pair_id": "sand_mana",
        "symbol_1": "SANDUSDT",
        "symbol_2": "MANAUSDT",
        "z_score": -2.72,
        "eg_p_value": 0.0031,
    },
    {
        "pair_id": "inj_atom",
        "symbol_1": "INJUSDT",
        "symbol_2": "ATOMUSDT",
        "z_score": 1.41,
        "eg_p_value": 0.0328,
    },
    {
        "pair_id": "trx_xlm",
        "symbol_1": "TRXUSDT",
        "symbol_2": "XLMUSDT",
        "z_score": -0.96,
        "eg_p_value": 0.0394,
    },
    {
        "pair_id": "etc_bch",
        "symbol_1": "ETCUSDT",
        "symbol_2": "BCHUSDT",
        "z_score": 2.18,
        "eg_p_value": 0.0106,
    },
    {
        "pair_id": "sui_apt",
        "symbol_1": "SUIUSDT",
        "symbol_2": "APTUSDT",
        "z_score": -1.35,
        "eg_p_value": 0.0253,
    },
    {
        "pair_id": "crv_uni",
        "symbol_1": "CRVUSDT",
        "symbol_2": "UNIUSDT",
        "z_score": 0.00,
        "eg_p_value": 0.0487,
    },
    {
        "pair_id": "btc_ltc",
        "symbol_1": "BTCUSDT",
        "symbol_2": "LTCUSDT",
        "z_score": 3.06,
        "eg_p_value": 0.0009,
    },
]

def format_pairs(pairs) -> str:
    """
    Формирует текст списка подходящих пар.

    Добавляет заголовок и нумерацию, выводит названия инструментов,
    z-score с двумя и EG p-value с четырьмя знаками после точки.
    Используется обработчиком списка пар для подготовки сообщения.
    При пустом списке возвращает заголовок с переносом строки.

    Args:
        pairs: list[dict] (содержит словари с полями symbol_1, symbol_2,
                          z_score и eg_p_value)

    Returns:
        str: Текст списка пар, разделённый переносами строк.
    """
    arr = ['Подходящие пары', '']
    for num, pair in enumerate(pairs, start=1):
        arr.append(f'{num}. {pair['symbol_1']} / {pair['symbol_2']} - z-score: {pair['z_score']:.2f};'
              f' EG p-value: {pair['eg_p_value']:.4f}')
    return '\n'.join(arr)


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

def find_pair(pairs, pair_id) -> dict | None:
    """
    Находит пару по идентификатору.

    Последовательно сравнивает поле pair_id каждого словаря с искомым
    значением. Возвращает первый совпавший словарь без создания копии.
    Используется обработчиком выбора пары для получения её показателей.

    Args:
        pairs: list[dict] (содержит словари пар с полем pair_id)
        pair_id: str (содержит идентификатор искомой пары)

    Returns:
        dict | None: Найденный словарь или None, если совпадений нет,
                     в том числе при пустом списке.
    """
    for pair in pairs:
        if pair['pair_id'] == pair_id:
            return pair
    return None

def get_page_pairs(pairs, page, page_size=5) -> list:
    start = page * page_size
    end = start + page_size
    return pairs[start:end]


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

@dp.callback_query(F.data == 'about')
async def about_handler(callback: CallbackQuery) -> None:
    """
    Показывает раздел о проекте.

    Подтверждает нажатие кнопки с данными about, затем заменяет текст
    сообщения заглушкой и прикрепляет кнопку главного меню.

    Args:
        callback: CallbackQuery (содержит данные нажатия и сообщение,
                                 текст которого требуется изменить)

    Returns:
        None: Не возвращает значение; изменяет сообщение в Telegram.
    """
    await callback.answer()
    await callback.message.edit_text('Здесь будет информация о нашем проекте',
                                     reply_markup=main_menu_keyboard)

@dp.callback_query(F.data == 'pairs')
async def pairs_handler(callback: CallbackQuery) -> None:
    """
      Показывает список подходящих пар.

      Подтверждает нажатие кнопки с данными pairs. Использует pairs_data,
      format_pairs и create_pairs_keyboard для замены текста сообщения
      списком учебных пар и прикрепления кнопок выбора.

      Args:
          callback: CallbackQuery (содержит событие запроса списка пар
                                   и связанное с кнопкой сообщение)

      Returns:
          None: Не возвращает значение; изменяет сообщение в Telegram.
      """
    await callback.answer()
    page_pairs = get_page_pairs(pairs_data, page=0)
    await callback.message.edit_text(format_pairs(page_pairs),
                                     reply_markup=create_pairs_keyboard(page_pairs))

@dp.callback_query(F.data.startswith('pairs_page:'))
async def pairs_page_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    page_number = int(callback.data.split(':', 1)[1])
    page_pairs = get_page_pairs(pairs_data, page_number)
    await callback.message.edit_text(format_pairs(page_pairs), reply_markup=create_pairs_keyboard(page_pairs))


@dp.callback_query(F.data == 'indicators')
async def indicators_handler(callback: CallbackQuery) -> None:
    """
        Показывает справочник показателей.

        Подтверждает нажатие кнопки с данными indicators и заменяет текст
        сообщения содержимым indicators_text. Прикрепляет кнопку возврата
        в главное меню. HTML-разметка обрабатывается согласно настройке бота.

        Args:
            callback: CallbackQuery (содержит событие открытия справочника
                                     и сообщение для редактирования)

        Returns:
            None: Не возвращает значение; изменяет сообщение в Telegram.
        """
    await callback.answer()
    await callback.message.edit_text(indicators_text,
                                     reply_markup=main_menu_keyboard)

@dp.callback_query(F.data == 'main_menu')
async def main_menu_handler(callback: CallbackQuery) -> None:
    """
        Возвращает пользователя в главное меню.

        Подтверждает нажатие кнопки с данными main_menu, заменяет текст
        сообщения приветствием Hello и прикрепляет основную клавиатуру.

        Args:
            callback: CallbackQuery (содержит событие возврата в меню
                                     и сообщение для редактирования)

        Returns:
            None: Не возвращает значение; изменяет сообщение в Telegram.
        """
    await callback.answer()
    await callback.message.edit_text('Hello', reply_markup=main_keyboard)



@dp.callback_query(F.data.startswith('pair:'))
async def selected_pair(callback: CallbackQuery) -> Message | bool:
    """
      Показывает сведения о выбранной паре.

      Подтверждает нажатие и извлекает идентификатор после первого
      двоеточия в callback.data. Ищет пару в pairs_data через find_pair.
      При наличии пары показывает инструменты, z-score и EG p-value,
      иначе выводит сообщение об отсутствии пары. В обоих случаях
      прикрепляет кнопку главного меню.

      Args:
          callback: CallbackQuery (содержит данные вида pair:ID
                                   и сообщение с кнопкой выбора)

      Returns:
          Message | bool: Результат редактирования сообщения. Для обычного
                          сообщения возвращается Message; API также
                          допускает True при редактировании inline-сообщения.
                          Текущий обработчик использует callback.message
                          и рассчитан на обычное сообщение в чате.
      """
    await callback.answer()
    pair_id = callback.data.split(':', 1)[1]
    pair = find_pair(pairs_data, pair_id)
    if pair is None:
        return await callback.message.edit_text('Пара не найдена',
                                                reply_markup=pair_keyboard)
    else:
        return await callback.message.edit_text(f'Выбрана пара: {pair['symbol_1']} / {pair['symbol_2']}\n'
                                                f'z-score: {pair["z_score"]}\n'
                                                f'EG p-value: {pair["eg_p_value"]}',
                                                reply_markup=pair_keyboard)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отправляет приветствие и главное меню по команде /start.

    Использует полное имя отправителя и экранирует его для HTML
    через html.quote. Отправляет новое сообщение с основной клавиатурой.
    Рассчитан на сообщение, у которого доступен отправитель from_user.

    Args:
        message: Message (содержит команду /start, сведения об отправителе
                          и чат для отправки приветствия)

    Returns:
        None: Не возвращает значение; отправляет сообщение в Telegram.
    """
    await message.answer(
        f"Hello, {html.quote(message.from_user.full_name)}!",
        reply_markup=main_keyboard
    )


async def main() -> None:
    """
    Создаёт бота и запускает получение обновлений.

    Использует TOKEN, загруженный из переменных окружения, и включает
    HTML-разметку по умолчанию. Передаёт бота диспетчеру dp и ожидает
    завершения polling. Вызывается через asyncio.run при запуске файла.

    Args:
        Отсутствуют.

    Returns:
        None: Не возвращает значение при штатном завершении polling.
    """
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
