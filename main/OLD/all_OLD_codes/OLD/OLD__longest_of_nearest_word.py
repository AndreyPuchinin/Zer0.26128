# Бежим по строке.
        # Потом для каждого символа бежим по всем картам.
        # Как только находим соответствие - кладем сразу всех их в all_matched_data.
        # Если следующий виток цикла начинается с того, что all_matched_data не пуст
        # (положили все, что начиналось с последнего перебранного символа строки),
        # Значит мы уже нашли все нужные вхождения.
        for i in range(len(sentence) - 1):
            if all_matched_data:  # те all_matched_data != []:
                longest_val = all_matched_data[0][0]
                longest_name = all_matched_data[0][1]
                longest_pos = all_matched_data[0][2]
                matched_card = all_matched_data[0][3]
                break
            for card in cards:
                for val in card.usual_vals:
                    if (i + len(val) <= len(sentence) and
                            sentence[i:i + len(val)] == val):
                        all_matched_data += [[val, card.name, i, card]]

        # Принимаем временно первое соответствие самым длинным
        # (для дальнейшего сравнения в цикле и нахождения истинно самого длинного соотвтствия)
        longest_string = all_matched_data[i][0]

        # Бежим по всем найденным соответствиям с первого (НЕ НУЛЕВОГО!!) по последнее
        # и сверяем каждое с нулевым,
        # Если текущее из цикла длиннее временно самого длинного (предполагаемо),
        # Обновляем потенциально самое длинное соответствие
        for i in range(len(all_matched_data) - 1):
            if len(all_matched_data[i + 1][0]) > len(longest_string):
                longest_string = all_matched_data[i + 1][0]
                longest_val = all_matched_data[i + 1][0]
                longest_name = all_matched_data[i + 1][1]
                longest_pos = all_matched_data[i + 1][2]
                matched_card = all_matched_data[i + 1][3]
