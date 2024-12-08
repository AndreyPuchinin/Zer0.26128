def longest_of_nearest_templ(self, inp_str: str, cards: List[Card]):
    # ищем самое длинное из всех самых близких вхождений
    # и формируем объект Swap
    # (см. в neuro_(...).py-файлах)

    longest_val = ""
    longest_name = ""
    longest_pos = 0
    matched_card = Card('', [])

    for card in cards:
        for one_template in card.templates:
            for i in range(len(inp_str) - len(one_template.val) + 1):
                if inp_str[i:i + len(one_template.val)] == one_template.val:
                    if len(one_template.val) > len(longest_val):
                        longest_val = one_template.val
                        longest_name = card.name
                        longest_pos = i
                        matched_card = card
                        break
    return Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)