def longest_of_nearest_val(self, inp_str: str, cards: List[Card]):
    # ищем самое длинное из всех самых близких вхождений
    # и формируем объект Swap
    # (см. в neuro_(...).py-файлах)

    longest_val = ""
    longest_name = ""
    longest_pos = 0
    matched_card = Card('', [])

    all_matched_data = []

    for card in cards:
        for val in card.usual_vals:
            for i in range(len(inp_str) - len(val) + 1):
                if inp_str[i:i + len(val)] == val:
                    all_matched_data += [[longest_val, longest_name, longest_pos, matched_card]]

    for i in range(len(all_matched_data) - 1):
        if len(all_matched_data[i + 1][0]) > len(all_matched_data[i][0]):
            longest_val = all_matched_data[i + 1][0]
            longest_name = all_matched_data[i + 1][1]
            longest_pos = all_matched_data[i + 1][2]
            matched_card = all_matched_data[i + 1][3]

    return Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)