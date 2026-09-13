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