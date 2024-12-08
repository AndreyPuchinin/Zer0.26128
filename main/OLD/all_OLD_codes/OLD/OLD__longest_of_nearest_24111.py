@staticmethod
    def _longest_of_nearest_val(sentence: str, words_data: List[List[str | Card]]):
        """1. Бежит по строке от позиции курсора (изначально = 0). \n
           2. Бежит для каждого символа по всем картам. \n
           3. Как только найдено первое совпадение:
           4. Запоминаем все эти карты. \n
           5. Продолжаем бежать по строке. \n
           6. Исключаем те карты, для которых следующий символ !=
               != следующему символу в строке. \n
           7. До тех пор, пока все оставшиеся значения не перестанут различаться.\n
           8. Если не найдено ни одного слова - вернуть None. \n
           8. Если найдено, и ровно ОДНО - тогда формируем свап из: \n
           8.1. входной строки (передается сюда через параметры), \n
           8.2. пустой строки в качестве новой для свапа (а может повторить входную?..), \n
           8.3. значения найденной в результате карточки, \n
           8.4. имени найденной в результате карточки, \n
           8.5. позиции найденной в результате карточки, \n
           8.6. саму найденную в результате карточку. \n
            \n
              Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)
            \n
              """

        # Проверим глазами, что ввод соответствует ожиданиям
        print(sentence)
        print(words_data)

        # задаем архив для совпадений
        matching_words_data = tuple()

        # позиция вхождения = 0
        first_match_pos = 0

        # Цикл, в котором ищется вхождения (внутренний), еще не стартовал
        cycle_started = False

        # ищем вхождения, пока они есть, то есть,
        # пока позиция текущего вхождения + длина любого вхождения (например, нулевого) не больше длины предложения
        # (стало быть, нужна проверка на не пустоту списка кандидатов)
        # или если список кандидатов пуст, но цикл уже начался
        # (стало быть нужна проверка на начало цикла)
        # или если цикл еще ни раз не начался
        while (not cycle_started or
               not matching_words_data and cycle_started and first_match_pos < len(sentence) or
               matching_words_data and first_match_pos + len(matching_words_data[0]) < len(sentence)):

            # Бежим по строке
            for i, char in enumerate(sentence[first_match_pos:]):

                # Если слов еще не найдено, находим те, которые начинаются с текущего символа
                if not matching_words_data:
                    matching_words_data = tuple([[item, words_data[1]][0] for item in words_data
                                                 if item[0].startswith(char)])

                # смотрим на промежуточный результат
                print(11, i, first_match_pos, char, matching_words_data)

                # продолжаем бежать по строке
                # (окунемся в этот цикл лишь на следующем витке из-за начального условия)
                # как только хотя бы 1 следующий символ в каком-то слове
                # не совпадает со следующим символом в строке,
                # дополняем это слово в архив несовпадений
                if first_match_pos != i and cycle_started:
                    mismatching_words_data = tuple(words_data for words_data in matching_words_data
                                                   if i - first_match_pos < len(words_data[0]) and
                                                   words_data[0][i - first_match_pos] != char)

                    # Смотрим на результат
                    print(22, i, first_match_pos, char, mismatching_words_data)

                    # и удаляем все несовпадения из списка кандидатов
                    matching_words_data = tuple(item for item in matching_words_data
                                                if item not in mismatching_words_data)

                    # Смотрим на результат
                    print(33, i, first_match_pos, char, matching_words_data)

                    # Если все потенциально первые вхождения кончились,
                    # Переходим к следующей позиции и прерываем внутренний цикл
                    if not matching_words_data:
                        first_match_pos += 1
                        break

                    # !!! - Далее НЮАНС:
                    # Согласно внутреннему механизму Зеро (А именно, благодаря CardManager'у)
                    # не может быть одинаковых значений (в рамках данной f() - слов)
                    # в одной или разных картах!!
                    # Это значит, что нужное слово будет окончательно найдено,
                    # как только слова перестанут различаться.
                    # Но set (tuple) не может содержать дубликатов, стало быть
                    # конец наступит, как только элемент останется единственный.
                    # НО!! Если конец строки наступил раньше, чем конец слов, их может остаться >1!
                    # Значит, если значение 1 - прерываем, а есть >1, обработаем после цикла
                    # ЕЩЕ РАЗ ОТМЕЧУ: это возможно ИСКЛЮЧИТЕЛЬНО благодаря внутреннему устройству Зеро!!
                    if len(matching_words_data) == 1:
                        word = matching_words_data[0][0]
                        if word in sentence:
                            print(44)
                            return matching_words_data

                # Запоминаем позицию первого совпадения некоторых слов по первому символу,
                # как только в первый раз нашли хоть какое-то совпадение
                if matching_words_data and not cycle_started:
                    first_match_pos = i
                    # отмечаем, что цикл стартовал
                    cycle_started = True

        # Архив совпадений содержит >1 слова, только если они не уложились в строку.
        # Тогда даже не станем их удалять - в строке не найдено ни одного целого слова!,
        # а просто вернем None.
        # Также не забудем о том, что совпадений может вообще не найтись,
        # а в этом случае число совпадений остается инициализированным -1!
        if 0 >= len(matching_words_data) or len(matching_words_data) > 1:
            print(55)
            return matching_words_data