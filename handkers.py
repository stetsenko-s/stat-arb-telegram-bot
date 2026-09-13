from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Dispatcher, html

from formatters import format_pairs
from pair_service import find_pair, get_page_pairs
from keyboards import create_pairs_keyboard, main_menu_keyboard, main_keyboard, pair_keyboard


router = Router()

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

@router.callback_query(F.data == 'about')
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

@router.callback_query(F.data == 'pairs')
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
                                     reply_markup=create_pairs_keyboard(page_pairs,
                                                                        page=0,
                                                                        total_pairs=len(pairs_data)
                                                                        )
                                     )

@router.callback_query(F.data.startswith('pairs_page:'))
async def pairs_page_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    page_number = int(callback.data.split(':', 1)[1])
    page_pairs = get_page_pairs(pairs_data, page_number)
    await callback.message.edit_text(format_pairs(page_pairs),
                                     reply_markup=create_pairs_keyboard(page_pairs,
                                                                        page=page_number,
                                                                        total_pairs=len(pairs_data)
                                                                        )
                                     )


@router.callback_query(F.data == 'indicators')
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

@router.callback_query(F.data == 'main_menu')
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

@router.callback_query(F.data.startswith('pair:'))
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


@router.message(CommandStart())
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