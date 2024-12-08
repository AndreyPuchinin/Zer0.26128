def _do_all_reverse_swaps(self, links_data: dict, templ_swap: Swap) -> None:
    """Использует информацию о ссылках и последней шаблонной замене, \n
        чтобы сделать одну обратную замену, \n
        а также добавляет обратный свап в поле self._swaps. \n
    \n
       Принимает: \n
       1. Словарь с именами и значениями ссылок. Если код доехал до сюда, значит коллизий НЕТ!!! \n
       2. Последнюю шаблонную замену \n
     \n
       Возвращает: \n
       None \n
     \n
       1. Создаем переменную под нужный шаблон, \n
           чтобы пучарм не ругался на неинициализированность \n
       2. Находим нужный шаблон \n
       3. Находим позицию шаблона в строке \n
       4. получаем доступ к позициям замен в замещающем значении шаблона \n
       5. Сортируем список позиций во избежание \n
          (и во избежание работаем с копией) \n
       6. Запоминаем последнюю версию строки для того, \n
           чтобы правильно сформировать обратный свап \n
       7. Производим финальную замену! \n
       8. Добавляем обратный свап в поле свапов"""

    # ВСПОМОГАТЕЛЬНАЯ СТРОКА!! УБРАТЬ!!
    # Смотрим на состояние параметров
    print(links_data, templ_swap.get_fields())

    # 1. Создаем переменную под нужный шаблон,
    #     чтобы пучарм не ругался на неинициализированность
    last_templ = []

    # 2. Находим нужный шаблон
    for one_templ in templ_swap.card.templates:
        if one_templ.name == templ_swap.replacing:
            last_templ = one_templ

    # 3. Находим позицию шаблона в строке
    templ_pos = self._str.find(last_templ.name)

    # 4. получаем доступ к позициям замен в замещающем значении шаблона
    for one_link in last_templ.links:

        # ВСПОМОГАТЕЛЬНАЯ СТРОКА!! УБРАТЬ!!
        # Смотрим на всякое-разное (меняю в процессе...)
        # print(one_link.non_terminal.get_fields())

        # 5. Сортируем список позиций во избежание
        #    (и во избежание работаем с копией)
        positions = one_link.non_terminal.positions.copy()
        positions.sort()
        for one_pos in positions:
            # 6. Запоминаем последнюю версию строки для того,
            #     чтобы правильно сформировать обратный свап
            prev_str = self._str

            # 7. Производим финальную замену!
            self._str = self._str[:templ_pos + one_pos] + list(links_data[one_link.non_terminal.the_link])[0] + \
                        self._str[templ_pos + one_pos + len(one_link.non_terminal.the_link):]

            # ВСПОМОГАТЕЛЬНАЯ СТРОКА!! УБРАТЬ!!
            # Смотрим на self._str
            # print(self._str)

            # 8. Добавляем обратный свап в поле свапов
            self._swaps += [Swap(prev_str, self._str, one_link.non_terminal.the_link,
                                 list(links_data[one_link.non_terminal.the_link])[0], one_pos,
                                 templ_swap.card)]