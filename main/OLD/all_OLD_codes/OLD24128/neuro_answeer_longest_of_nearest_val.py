def longest_of_nearest_val(inp_str: str, cards: List[Card]) -> Swap:
    longest_val = ""
    longest_name = ""
    longest_pos = 0

    for card in cards:
        for i in range(len(inp_str) - len(card.vals) + 1):
            if inp_str[i:i + len(card.vals)] == card.vals:
                if len(card.vals) > len(longest_val):
                    longest_val = card.vals
                    longest_name = card.link_name
                    longest_pos = i
                    break

    return Swap(longest_val, longest_name, longest_pos)


"""Объяснение:
Инициализируем переменные longest_val, longest_name и longest_pos, которые будут хранить самое длинное значение, имя карты и позицию вхождения соответственно.
Проходим по всем картам в списке cards.
Для каждой карты проверяем, есть ли ее значение card.vals в строке inp_str. Делаем это, проходя по всем возможным позициям в inp_str и сравнивая подстроку длины len(card.vals) с card.vals.
Если найдено совпадение, то проверяем, является ли длина card.vals больше, чем длина longest_val. Если да, то обновляем longest_val, longest_name и longest_pos.
После прохода по всем картам, возвращаем объект Swap с найденными значениями.
Таким образом, функция находит самое длинное из всех самых близких значений всех карт и формирует объект Swap с этим значением, именем подходящей карты и позицией вхождения значения в строку inp_str."""