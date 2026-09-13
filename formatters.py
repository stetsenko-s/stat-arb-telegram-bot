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