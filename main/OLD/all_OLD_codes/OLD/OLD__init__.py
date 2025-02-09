from typing import List


# from pprint import pprint

# SELF(REF!) = самоссылка
# Link = ссылка

# Одно значение шаблона:
# строка значения и позиция
class LinkFiniteFields:
    """Одно значение шаблона:
       строка значения и позиция"""

    def __init__(self, the_link: str, pos: List[int]):
        self.the_link = the_link
        self.pos = pos

    def get_fields(self):
        return [self.the_link, self.pos]


# Ссылка: имя и значение. Каждое содержит строку значения и позицию
class TemplValLinkData:
    """Ссылка: имя и значение. Каждое содержит строку значения и позицию"""

    def __init__(self, name_links: LinkFiniteFields, val_links: LinkFiniteFields):
        self.name_links = name_links
        self.val_links = val_links

    def get_fields(self):
        return [
            [link for link in self.name_links.get_fields()],
            [link for link in self.val_links.get_fields()]
        ]


# Шаблонное значение: строка имени, строка значения
# и информация о ссылках внутри шаблонного значения
class TemplValData:
    """Шаблонное значение: строка имени, строка значения
       и информация о ссылках внутри шаблонного значения"""

    def __init__(self, name: str, val: str, many_temp_links: List[TemplValLinkData]):
        self.name = name
        self.val = val
        self.some_temp_links = many_temp_links

    def get_fields(self):
        return [self.name, self.val,
                [one_temp_link.get_fields() for one_temp_link in self.some_temp_links]
                ]


class Card:
    def __init__(self, name: str, vals: List[str]):
        self.name = name
        self.usual_vals = []
        self.selfrefs = []
        self.templates = []
        self.templ_refs = []  # по идее можно дополнить в selfrefs, а потом в templates
        for val in vals:
            self._check_and_classify_val(val)

    def _check_and_classify_val(self, val: str):
        # ВРЕМЕННО все значения = usual
        self.usual_vals += [val]

    def get_fields(self):
        return [self.name,
                self.usual_vals,

                # TemplVal
                [selfrefs.get_fields() for selfrefs in self.selfrefs],

                # TemplVal:
                [template.get_fields() for template in self.templates],

                self.templ_refs]


class CardManager:
    def __init__(self):
        pass

    def check_card(self):
        pass

    def add_card(self):
        pass


class Errors:
    def __init__(self):
        self._errors = []

        self._no_errors = 'Успешно, ошибок нет!'
        # ...
        pass

    def get_fields(self):
        return self._errors

    def merge_with_other_errors_obj(self, other_errors_obj):
        if other_errors_obj.get_fields():  # != []:
            self.caught_errors()
        for one_error in other_errors_obj.get_fields():
            self._errors += [one_error]

    def no_errors(self):
        self._errors = [self._no_errors]
        return self._errors

    def caught_errors(self):
        while self._no_errors in self._errors:
            self._errors.remove(self._no_errors)

    def collision(self, link_name: str, link_vals: List[str]):
        self.caught_errors()
        res_str = 'Коллизия! Неясно, на что заменять \'' + link_name + '\' - на \'' + link_vals[0] + '\''
        for one_link_val in link_vals[1:-1]:
            res_str += ', \'' + one_link_val + '\''
        res_str += ' или \'' + link_vals[-1] + '\''
        self._errors += [res_str]
        return self._errors

    # def error_type_1(self):
    #     self.errors += [self.error_type_1]
    #     return self.errors


class Swap:
    def __init__(self, prev_str: str, cur_str: str, link_val, link_name, pos, card: Card):
        self.prev_str = prev_str
        self.cur_str = cur_str
        self.link_val = link_val
        self.link_name = link_name
        self.pos = pos
        self.card = card

    def get_fields(self):
        return [self.prev_str,
                self.cur_str,
                self.link_val,
                self.link_name,
                self.pos,
                self.card.get_fields()]


# Хранит
# Первую строку,
# последнюю успешную
# и пользовательскую
class ResStrStruct:
    def __init__(self, first_str: str, last_successful: str, user_str: str):
        self.first_str = first_str
        self.last_successful = last_successful
        # self.empty = ''
        self.user_str = user_str

    def get_fields(self):
        return [self.first_str,
                self.last_successful,
                # self.empty,
                self.user_str]


# Свапы,
# 3строки (класс ResStrStruct выше)
# и ошибки
class Result:
    def __init__(self, swaps: list[Swap], res_str: ResStrStruct, errors: Errors):
        self.swaps = swaps
        self.res_str = res_str
        self.errors = errors

    def get_fields(self):
        return [[swap.get_fields() for swap in self.swaps], self.res_str.get_fields(), self.errors.get_fields()]


class str_Name_and_Val:
    def __init__(self, name: str, val: str):
        self.name = name
        self.val = val

    def get_fields(self):
        return [self.name, self.val]


class str_Names_and_Vals:
    def __init__(self):
        self.str_names_and_vals_list = []

    def add_el(self, str_names_and_vals: str_Name_and_Val):
        self.str_names_and_vals_list += [str_names_and_vals]

    def get_fields(self):
        return [one_list_el.get_fields() for one_list_el in self.str_names_and_vals_list]


class SelfrefErrorSeq:
    def __init__(self):
        self.dict = dict()

    def add_link(self, name: str, vals: dict[str]) -> None:
        if name not in self.dict.keys():
            self.dict[name] = []
        self.dict[name] += [val for val in vals]

    # Удаляет только одно значение
    # (даже если их много совпадающих)
    # Если значение не найдено, кинет False. Иначе - True
    def del_val(self, name, val) -> bool:
        if name in self.dict.keys():
            if val in self.dict[name]:
                self.dict[name].remove(val)
                return True
        return False

    def get_dict(self):
        return self.dict

    def _link_name_reverse(self, res_name: List[str]):
        while '' in res_name:
            res_name.remove('')
        print(res_name)
        res_name_str_reversed = ''
        for _str in res_name:
            res_name_str_reversed += _str
        for _str_i in range(len(res_name) // 4):
            res_name[_str_i * 2 + 1], res_name[len(res_name) - _str_i * 2 - 2] = \
                res_name[len(res_name) - _str_i * 2 - 2], res_name[_str_i * 2 + 1]
        res_name_str = ''
        for _str in res_name:
            res_name_str += _str
        return res_name_str, res_name_str_reversed

    def get_fields(self):
        return self.dict


class SelfrefLinksData:
    """Информация о ссылке самоссылки:
       первичное имя и все конечные значения"""

    def __init__(self, get_selfrefs_links_one_name, _link_name_reverse):
        self.links = SelfrefErrorSeq()
        self._get_selfrefs_links_one_name = get_selfrefs_links_one_name
        self._link_name_reverse = _link_name_reverse

    # Перенес в SelfrefErrorSeq УДАЛИТЬ!!!
    # def add_link_data(self, name: str, vals: List[str]) -> None:
    #     if name not in self.links.keys():
    #         self.links[name] = []
    #     self.links[name] += [val for val in vals]

    # возвращает словарь: имя = имя ссылки,
    #                     значение = список: первый элемент повторяет ключ
    #                                        далее - все конечные значения
    #                                        если хотя бы одно значение далее разнится - КОЛЛИЗИЯ!!
    def get_links_data(self, used_templ: TemplValData, swaps: List[Swap]):
        for one_link in used_templ.some_temp_links:
            self.links.get_dict()[one_link.val_links.the_link] = [one_link.val_links.the_link]
        # print(self.links)
        # print(links_names)
        prev_links = -1
        i = 0

        _str_names_and_vals = str_Names_and_Vals()
        for other_swap in swaps:
            str_names_and_vals = str_Name_and_Val(other_swap.link_val, other_swap.link_name)
            _str_names_and_vals.add_el(str_names_and_vals)

        _str_names_and_vals = _str_names_and_vals.get_fields()
        # print(_str_names_and_vals)
        while i < len(swaps[-2:: -1]):
            # Процедура сочленения значений столько раз,
            # сколько их есть в самоссылке
            one_swap = swaps[-2:: -1][i]
            if one_swap.card.selfrefs:  # != []
                primary_name, res_name_list = self._get_selfrefs_links_one_name(_str_names_and_vals,
                                                                                one_swap)
                res_name, res_name_reversed = self._link_name_reverse(res_name_list)
                if primary_name != '':  # and res_name != ''  # and res_name_reversed != '':
                    self.links.get_dict()[primary_name] += [res_name]  # [[res_name, res_name_reversed]]
            else:
                for one_link_name in self.links.get_dict():
                    for other_link_name in self.links.get_dict()[one_link_name]:
                        # если текущая позиция совпадает с последней,
                        # значит ссылка та же, но более глубокое значение
                        if one_swap.link_name == other_link_name:
                            if prev_links == one_swap.pos:
                                self.links.get_dict()[one_link_name].remove(one_swap.link_name)
                            self.links.get_dict()[one_link_name] += [one_swap.link_val]
                            # print(links_names)
                prev_links = one_swap.pos
            i += 1
        for one_key in self.links.get_dict().keys():
            self.links.del_val(one_key, one_key)
        # print(self.links.get_fields())
        # return self.links

    def get_fields(self) -> SelfrefErrorSeq:
        return self.links


# Ради collision_check(...)
class CollisionInfo:
    def __init__(self):
        self._res = None
        self._result_reverse_swap = dict()
        # self._links = SelfrefLinksData(lambda: ('', ''), lambda: ('', ''))
        self._errors = Errors()

    def get_res(self):
        return self._res

    def get_result_reverse_swap(self):
        return self._result_reverse_swap

    def get_errors(self):
        return self._errors

    def collision_check(self, links_data: SelfrefLinksData):
        # self._links = links_data
        # links_res = {}
        caught_error = False
        caught_error_links_names = []
        for one_link_name in links_data.links.get_dict():
            # print(one_link_name)
            # В links_data[one_link_name] лежит имя ссылки (one_link.val_links.the_link), а после
            # все значения ссылки
            # Иначе (если первый элемент другой) не работает цикл выше (теперь get_link_names),
            # (не выполняет то, что должно)
            # При этом каждое значение ссылки - конечное.
            # То есть если есть разные концы (сначала отрезать имя в первой ячейке), КОЛЛИЗИЯ
            for other_link_name in links_data.links.get_dict()[one_link_name][1:]:
                # Проверка на коллизию:
                # Если да,
                # то сразу накапливаем ошибку в self._res.errors!
                if other_link_name != links_data.links.get_dict()[one_link_name][0] and \
                        one_link_name not in caught_error_links_names:
                    caught_error = True
                    error_names = links_data.links.get_dict()[one_link_name].copy()
                    error_names.reverse()
                    # print(error_names)
                    error_names_without_doubles = []
                    for one_error_name in error_names:
                        if one_error_name not in error_names_without_doubles:
                            error_names_without_doubles.append(one_error_name)
                    # print(error_names_without_doubles)
                    self._errors.collision(one_link_name, error_names_without_doubles)
                    caught_error_links_names += [one_link_name]
                else:
                    self._result_reverse_swap[one_link_name] = links_data.links.get_dict()[one_link_name][-1]
        # print(self._result_reverse_swap)
        if not caught_error:
            self._res = True
            # print([True, links_res])
            # return [True, links_res]
        else:
            self._res = False
            # print([False, {}])
            # return [False, {'a': 1}]

    def get_fields(self):
        return [self._res, self._result_reverse_swap, self._errors]


# Возвращает список из 2ух полей [что заменяли, на что заменяли]
class OneLinkSwapInfo:
    def __init__(self, name: str, val: str):
        self.name = name
        self.val = val


# возвращает словарь:
# левое поле - позиция
# правое - список из 2ух полей [что заменяли, на что заменяли]
class LinksSwapsInfo:
    def __init__(self):
        self.links_swaps_info = dict()

    def add_swap(self, pos, name, val):
        if pos not in self.links_swaps_info.keys():
            self.links_swaps_info[pos] = [name, val]
        else:
            if [name, val] not in self.links_swaps_info[pos]:
                self.links_swaps_info[pos] += [name, val]

    def get_reverse_links(self, reverse_links: TemplValData, collision_obj: dict):
        # сортирует все pos в name_links
        # возвращает словарь, где левое поле - pos,
        # правое - список [что заменяли, на что заменяли]
        # print(collision_obj)
        # print(reverse_links.get_fields())
        for one_temp_link in reverse_links.some_temp_links:
            # print(one_temp_link.get_fields())
            if one_temp_link.name_links.the_link in collision_obj.keys():
                for one_pos in one_temp_link.name_links.pos:
                    one_link_swap_info = OneLinkSwapInfo(one_temp_link.name_links.the_link,
                                                         collision_obj[one_temp_link.name_links.the_link])
                    self.add_swap(one_pos, one_link_swap_info.name, one_link_swap_info.val)
        # print(self.links_swaps_info)
        return self.links_swaps_info

    def get_fields(self):
        return self.links_swaps_info


class Parser:
    # инициализирует все поля
    def __init__(self, cards: List[Card], inp_str: str):
        self._cards = cards
        self._first_str = inp_str
        self._user_str = None
        self._str = inp_str
        self._swaps = []
        self._errors = Errors()
        self._errors.no_errors()
        self._res = Result([], ResStrStruct('', '', ''), self._errors)

    # находит самое длинное из всех самых близких обычных значений во входной строке
    def longest_of_nearest_val(self, inp_str: str, cards: List[Card]) -> Swap:
        # ищем самое длинное из всех самых близких вхождений
        # и формируем объект Swap
        # (см. в neuro_(...).py-файлах)

        longest_val = ""
        longest_name = ""
        longest_pos = 0
        matched_card = Card('', [])

        all_matched_data = []

        # бежим по строке
        # потом для каждого символа бежим по всем картам
        # как только находим соответствие - кладем все в all_matched_data
        # если следующий виток цикла начинается с того, что all_matched_data не пуст
        # значит мы уже нашли все нужные вхождения
        for i in range(len(inp_str) - 1):
            if all_matched_data:  # те all_matched_data != []:
                longest_val = all_matched_data[0][0]
                longest_name = all_matched_data[0][1]
                longest_pos = all_matched_data[0][2]
                matched_card = all_matched_data[0][3]
                break
            for card in cards:
                for val in card.usual_vals:
                    if (i + len(val) <= len(inp_str) and
                            inp_str[i:i + len(val)] == val):
                        all_matched_data += [[val, card.name, i, card]]

        for i in range(len(all_matched_data) - 1):
            if len(all_matched_data[i + 1][0]) > len(all_matched_data[i][0]):
                longest_val = all_matched_data[i + 1][0]
                longest_name = all_matched_data[i + 1][1]
                longest_pos = all_matched_data[i + 1][2]
                matched_card = all_matched_data[i + 1][3]

        return Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)

    # находит самое длинное из всех самых близких шаблонных значений во входной строке
    # КОПИПАСТА с longest_of_nearest_val!!! Разница лишь в:
    # for one_template in card./-templates-/: ...
    def longest_of_nearest_templ(self, inp_str: str, cards: List[Card]) -> Swap:
        # ищем самое длинное из всех самых близких вхождений
        # и формируем объект Swap
        # (см. в neuro_(...).py-файлах)

        longest_val = ""
        longest_name = ""
        longest_pos = 0
        matched_card = Card('', [])

        all_matched_data = []

        # бежим по строке
        # потом для каждого символа бежим по всем картам
        # как только находим соответствие - кладем все в all_matched_data
        # если следующий виток цикла начинается с того, что all_matched_data не пуст
        # значит мы уже нашли все нужные вхождения
        for i in range(len(inp_str) - 1):
            if all_matched_data:  # те all_matched_data != []:
                longest_val = all_matched_data[0][0]
                longest_name = all_matched_data[0][1]
                longest_pos = all_matched_data[0][2]
                matched_card = all_matched_data[0][3]
                break
            for card in cards:
                for one_template in card.templates:
                    for one_templ_link in one_template.links:
                        if (i + len(one_template.val) <= len(inp_str) and
                                inp_str[i:i + len(one_template.val)] == one_template.val):
                            all_matched_data += [[one_template.val, one_template.name, i, card]]

        for i in range(len(all_matched_data) - 1):
            if len(all_matched_data[i + 1][0]) > len(all_matched_data[i][0]):
                longest_val = all_matched_data[i + 1][0]
                longest_name = all_matched_data[i + 1][1]
                longest_pos = all_matched_data[i + 1][2]
                matched_card = all_matched_data[i + 1][3]

        return Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)

    # находит самое длинное из всех самых близких значений-самоссылок во входной строке
    # КОПИПАСТА с longest_of_nearest_val!!! Разница лишь в:
    # for val in card./-selfrefs-/: ...
    def longest_of_nearest_selfrefs(self, inp_str: str, cards: List[Card]) -> Swap:
        # ищем самое длинное из всех самых близких вхождений
        # и формируем объект Swap
        # (см. в neuro_(...).py-файлах)

        longest_val = ""
        longest_name = ""
        longest_pos = 0
        matched_card = Card('', [])

        all_matched_data = []

        # бежим по строке
        # потом для каждого символа бежим по всем картам
        # как только находим соответствие - кладем все в all_matched_data
        # если следующий виток цикла начинается с того, что all_matched_data не пуст
        # значит мы уже нашли все нужные вхождения
        for i in range(len(inp_str) - 1):
            if all_matched_data:  # те all_matched_data != []:
                longest_val = all_matched_data[0][0]
                longest_name = all_matched_data[0][1]
                longest_pos = all_matched_data[0][2]
                matched_card = all_matched_data[0][3]
                break
            for card in cards:
                for val in card.selfrefs:
                    # print(inp_str[i:i + len(val)], '|', val)
                    if (i + len(val.the_link) <= len(inp_str) and
                            inp_str[i:i + len(val.the_link)] == val.the_link):
                        all_matched_data += [[val.the_link, card.name, i, card]]

        for i in range(len(all_matched_data) - 1):
            if len(all_matched_data[i + 1][0]) > len(all_matched_data[i][0]):
                longest_val = all_matched_data[i + 1][0]
                longest_name = all_matched_data[i + 1][1]
                longest_pos = all_matched_data[i + 1][2]
                matched_card = all_matched_data[i + 1][3]

        return Swap(inp_str, '', longest_val, longest_name, longest_pos, matched_card)

    # ПРЯМЫЕ ЗАМЕНЫ (параметр указывает тип прямых замен:
    #                обычные, самоссыльные или шаблонные)
    def _simple_swaps(self, longest_of_nearest) -> None:
        while True:
            # print(self._str)
            found_val = longest_of_nearest(self._str, self._cards)
            if found_val.get_fields() == Swap(self._str, '', '', '', 0, Card('', [])).get_fields():
                break
            else:
                # print(found_val.get_fields())
                # input()
                self._str = self._str.replace(found_val.link_val, found_val.link_name, 1)
                self._swaps += [found_val]
                self._swaps[-1].cur_str = self._str
                # input()
        self._res = Result(self._swaps, ResStrStruct(self._first_str, self._str, self._user_str), self._errors)

    # ПРЯМЫЕ ЗАМЕНЫ САМОССЫЛОК
    # (использует параметризированный _simple_swaps)
    def _selfrefs_swaps(self) -> None:
        # тут пригодился бы полиморфизм
        # замены по самоссылкам
        self._simple_swaps(self.longest_of_nearest_selfrefs)
        # если замен по шаблону не произошло, строка настраивается

    # ШАБЛОННЫЕ ЗАМЕНЫ
    # (использует параметризированный _simple_swaps)
    def _templates_swaps(self) -> None:
        # тут пригодился бы полиморфизм
        # шаблонные замены
        self._simple_swaps(self.longest_of_nearest_templ)
        # если замен по шаблону не произошло, строка настраивается

    # Действие между ПРЯМЫМИ и ОБРАТНЫМИ заменами:
    # находит шаблон из последнего свапа
    def _get_used_templ(self, last_templ_swap: Swap) -> TemplValData:
        for one_swap in self._swaps[-2: 0: -1]:
            # перебираем все шаблоны
            for one_templ in last_templ_swap.card.templates:
                for one_link in one_templ.links:
                    # print(one_link.get_fields())
                    # print(one_swap.link_name)
                    # print()
                    # ищем тот, который используется
                    if one_link.name_links.the_link == one_swap.link_name:
                        # print(one_templ.get_fields())
                        return one_templ
        # Если None - значит ни один шаблон не использовался в последней простой замене

    # ??????
    def _link_name_reverse(self, res_name: List[str]):
        while '' in res_name:
            res_name.remove('')
        # print(res_name)
        res_name_str_reversed = ''
        for _str in res_name:
            res_name_str_reversed += _str
        for _str_i in range(len(res_name) // 4):
            res_name[_str_i * 2 + 1], res_name[len(res_name) - _str_i * 2 - 2] = \
                res_name[len(res_name) - _str_i * 2 - 2], res_name[_str_i * 2 + 1]
        res_name_str = ''
        for _str in res_name:
            res_name_str += _str
        return res_name_str, res_name_str_reversed

    # Находит первичное и конечное имя от
    def get_selfrefs_links_one_name(self, _links_name_and_val, one_swap: Swap):
        # print('!!!')
        res_name = []
        primary_name = ''
        primary_val = ''
        cur_name = ''
        # print(len(_links_name_and_val), _links_name_and_val)
        # перебираем самоссылки (может быть одна)
        for one_ref in one_swap.card.selfrefs:
            # прибавляем остаток ( '(' в начале '(число-число)' )
            res_name = [one_ref.the_link[one_ref.positions[0] - 1]]
            # print('!')
            for j in range(len(one_ref.positions)):
                if one_swap.link_val == one_ref.the_link:
                    # print(_links_name_and_val)
                    cur_name = one_ref.the_link
                    # print(cur_name)
                    primary_name = ''
                    primary_val = ''
                    for one_link in reversed(_links_name_and_val):
                        if one_link[0] == cur_name:
                            primary_name = one_link[1]
                            primary_val = one_link[0]
                            # print(primary_val, primary_name)
                            cur_name = primary_name
                            # print(1, one_ref.the_link[len(primary_name)+1: one_ref.pos[j-1]])
                            break
                    # print(primary_name)
                    # число -> один -> 1
                    # ПРЕДПОЛОЖЕНИЕ, ЧТО ДАЛЬШЕ 1 МОЖНО ИСКАТЬ СКОЛЬКО УГОДНО,
                    # и НИЧЕГО НЕ БУДЕТ НАЙДЕНО!! (По идее должно быть так)
                    # print('!')
                    k = len(_links_name_and_val[:-1]) - 1
                    while k >= 0:
                        one_link = _links_name_and_val[k]
                        # print(one_link)
                        # 0  n-1
                        # for k, one_link in enumerate(reversed(_links_name_and_val[:-1])):
                        # print(one_link, cur_name)
                        if len(one_link) > 1 and one_link[1] == cur_name and \
                                _links_name_and_val[k] != [primary_val, primary_name]:
                            cur_name = _links_name_and_val[k][0]

                            # print(one_ref.the_link[len(primary_name)+1: one_ref.pos[j - 1]])
                            # print(1, res_name)
                            del _links_name_and_val[k]
                            k += 1
                            # print('del', _links_name_and_val[k])
                            # print(cur_name)
                        k -= 1
                    res_name += [cur_name]
                    res_name += [one_ref.the_link[len(primary_name) + 1: one_ref.positions[j - 1]]]
            res_name += [one_ref.the_link[one_ref.positions[-1] + len(primary_name):]]
            # print(one_ref.the_link[one_ref.pos[-1] + len(primary_name):])
            # print(res_name)
            # print(one_ref.the_link[one_ref.pos[-1]+len(cur_name)+1:])
            # print(len(_links_name_and_val), _links_name_and_val)
        # res_name_str = self._link_name_reverse(res_name)
        # print(primary_name, res_name)
        return primary_name, res_name

    # создает и использует объект класса SelfrefLinksData
    # проверяет равенство всех значений ссылок самоссылки
    # копит ошибку, если надо
    def _not_collision(self, used_templ: TemplValData) -> CollisionInfo:
        links_data = SelfrefLinksData(self.get_selfrefs_links_one_name,
                                      self._link_name_reverse)
        # print(links_data.get_fields())
        links_data.get_links_data(used_templ, self._swaps)
        # print(links_data.get_fields())
        # print(links_data)
        collision_info = CollisionInfo()
        collision_info.collision_check(links_data)
        return collision_info

    # ОБРАТНЫЕ ЗАМЕНЫ
    def _reverse_swaps(self):
        if self._swaps and self._swaps[len(self._swaps) - 1].card.templates != []:
            res_str = self._res.res_str.last_successful
            last_templ_swap = self._swaps[len(self._swaps) - 1]
            one_used_templ = self._get_used_templ(last_templ_swap)
            # print(one_used_templ.get_fields())
            collision_info = self._not_collision(one_used_templ)
            collision_res = collision_info.get_res()
            collision_res_rev_swap = collision_info.get_result_reverse_swap()
            self._errors.merge_with_other_errors_obj(collision_info.get_errors())
            # print(collision_obj)
            if collision_res:
                reverse_links = LinksSwapsInfo().get_reverse_links(one_used_templ, collision_res_rev_swap)
                # print(reverse_links)
                while reverse_links:
                    prev_str = res_str
                    cur_pos = max(reverse_links.keys())
                    link_val = reverse_links[cur_pos][1]
                    link_name = reverse_links[cur_pos][0]
                    res_str = prev_str[:cur_pos + 1]
                    res_str += link_val
                    res_str += prev_str[cur_pos + len(link_name) + 1:]
                    del reverse_links[cur_pos]
            self._res.res_str.last_successful = res_str

    # ВСЕ ЗАМЕНЫ
    def start_warp_drive(self, user_str: str):
        self._user_str = user_str
        self._simple_swaps(self.longest_of_nearest_val)
        self._selfrefs_swaps()
        self._templates_swaps()
        self._reverse_swaps()
        # for swap in self._swaps:
        #     pprint(swap.get_fields()[2:5])
        return self._res


class Tests:
    def __init__(self):
        pass

    def run_all_tests(self):
        print('#0', self.test_0(), '\n')
        print('#1', self.test_1(), '\n')
        print('#11', self.test_11(), '\n')
        print('#2', self.test_2(), '\n')
        print('#21', self.test_21(), '\n')
        print('#3', self.test_3(), '\n')
        print('#31', self.test_31(), '\n')
        print('#32', self.test_32(), '\n')
        print('#4', self.test_4(), '\n')
        print('#41', self.test_41(), '\n')
        print('#42', self.test_42(), '\n')

        # print('#5', self.test_5(), '\n')

        # print('#6', self.test_6(), '\n')
        # print('#7', self.test_7(), '\n')
        # print('#8', self.test_8(), '\n')

    def test_0(self):
        card1 = Card('число', ['один'])
        inp_str = '.1'
        user_str = 'user_str'
        swaps = []
        res_str = '.1'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        # print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        # print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    def test_1(self):
        card1 = Card('число', ['один', '1'])
        inp_str = '.один'
        user_str = 'user_str'
        swaps = [Swap('.один', '.число', 'один', 'число', 1, card1)]
        res_str = '.число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        # print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        # print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    def test_11(self):
        card1 = Card('число', ['один', 'два'])
        inp_str = '.один плюс один'
        user_str = 'user_str'
        swaps = [Swap('.один плюс один', '.число плюс один', 'один', 'число', 1, card1),
                 Swap('.число плюс один', '.число плюс число', 'один', 'число', 12, card1)]
        res_str = '.число плюс число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        # print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        # print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # temple test (pos)
    def test_2(self):
        card1 = Card('число', ['один', 'два'])
        card2 = Card('дважды число', [])
        one_name_links = LinkFiniteFields('число', [7])
        one_vals_links = LinkFiniteFields('число', [0, 11])
        many_temp_links = TemplValLinkData(one_name_links, one_vals_links)
        user_str = 'user_str'
        card2.templates = [TemplValData('дважды число', 'число плюс число',
                                        [many_temp_links])]
        inp_str = '.один плюс один.'

        swaps = [Swap('.один плюс один.', '.число плюс один.',
                      'один', 'число', 1, card1),
                 Swap('.число плюс один.', '.число плюс число.',
                      'один', 'число', 12, card1),
                 #
                 # templ_swap
                 Swap('.число плюс число.', '.дважды число.',
                      'число плюс число', 'дважды число', 1, card2)
                 #
                 # reverse swaps
                 # Swap('.дважды число.', '.дважды один.',
                 #     'один', 'число', 7, card2),
                 ]
        res_str = '.дважды один.'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # poly links-typed templ test (pos)
    def test_21(self):
        card1 = Card('число', ['один', 'два'])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkFiniteFields('число', [8])
        vals_links1 = LinkFiniteFields('число', [0, 22])
        name_links2 = LinkFiniteFields('слово', [31, 19])
        vals_links2 = LinkFiniteFields('слово', [11, 33, 44])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)
        card2_link2 = TemplValLinkData(name_links2, vals_links2)

        card2.templates = [TemplValData('дважды (число плюс слово) плюс слово',
                                        'число плюс слово плюс число плюс слово плюс слово',
                                        [card2_link1, card2_link2])]
        inp_str = '.1 плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [Swap('.1 плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '1', 'один', 1, card4),
                 Swap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      'один', 'число', 1, card1),
                 Swap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс 1 плюс абракадабра плюс абракадабра', 'абракадабра',
                      'слово', 12, card3),
                 Swap('.число плюс слово плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                      '1', 'один', 23, card4),
                 Swap('.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                      'один', 'число', 23, card1),
                 Swap('.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс число плюс слово плюс абракадабра', 'абракадабра',
                      'слово', 34, card3),
                 Swap('.число плюс слово плюс число плюс слово плюс абракадабра',
                      '.число плюс слово плюс число плюс слово плюс слово', 'абракадабра',
                      'слово', 45, card3),

                 # templ_swap
                 Swap('.число плюс слово плюс число плюс слово плюс слово',
                      '.дважды (число плюс слово) плюс слово',
                      'число плюс слово плюс число плюс слово плюс слово',
                      'дважды (число плюс слово) плюс слово',
                      1, card2)

                 # reverse swaps
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (число плюс слово) плюс абракадабра',
                 #      'абракадабра', 'слово', 32, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра) плюс слово',
                 #      'абракадабра', 'слово', 19, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра)',
                 #      '1', 'число', 8, card2),
                 ]
        res_str = '.дважды (1 плюс абракадабра) плюс абракадабра'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # collision one link pos test
    def test_3(self):
        card1 = Card('число', ['один', 'два'])
        # card2 = Card('дважды число', ['число плюс число'])
        card2 = Card('дважды число', [])

        name_links1 = LinkFiniteFields('число', [7])
        vals_links1 = LinkFiniteFields('число', [0, 11])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)

        card2.templates += [TemplValData('дважды число', 'число плюс число', [card2_link1])]

        inp_str = '.один плюс два.'
        user_str = 'user_str'
        swaps = [
            # прямые замены
            Swap('.один плюс два.', '.число плюс два.', 'один', 'число', 1, card1),
            Swap('.число плюс два.', '.число плюс число.', 'два', 'число', 12, card1),

            # шаблонные замены
            Swap('.число плюс число.', '.дважды число.', 'число плюс число', 'дважды число', 1, card2)
        ]
        res_str = '.дважды число.'  # в 3 тесте эта строка настраивается юзером!
        error = Errors()
        error.collision('число', ['один', 'два'])
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # collision polytyped links pos test
    def test_31(self):
        card1 = Card('число', ['один', 'два'])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkFiniteFields('число', [8])
        vals_links1 = LinkFiniteFields('число', [0, 22])
        name_links2 = LinkFiniteFields('слово', [31, 19])
        vals_links2 = LinkFiniteFields('слово', [11, 33, 44])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)
        card2_link2 = TemplValLinkData(name_links2, vals_links2)

        card2.templates = [TemplValData('дважды (число плюс слово) плюс слово',
                                        'число плюс слово плюс число плюс слово плюс слово',
                                        [card2_link1, card2_link2])]
        inp_str = '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [Swap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      'один', 'число', 1, card1),
                 Swap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс 1 плюс абракадабра плюс абракадабра', 'абракадабра',
                      'слово', 12, card3),
                 Swap('.число плюс слово плюс 1 плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                      '1', 'один', 23, card4),
                 Swap('.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                      'один', 'число', 23, card1),
                 Swap('.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                      '.число плюс слово плюс число плюс слово плюс абракадабра', 'абракадабра',
                      'слово', 34, card3),
                 Swap('.число плюс слово плюс число плюс слово плюс абракадабра',
                      '.число плюс слово плюс число плюс слово плюс слово', 'абракадабра',
                      'слово', 45, card3),

                 # templ_swap
                 Swap('.число плюс слово плюс число плюс слово плюс слово',
                      '.дважды (число плюс слово) плюс слово',
                      'число плюс слово плюс число плюс слово плюс слово',
                      'дважды (число плюс слово) плюс слово',
                      1, card2)

                 # reverse swaps
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (число плюс слово) плюс абракадабра',
                 #      'абракадабра', 'слово', 32, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра) плюс слово',
                 #      'абракадабра', 'слово', 19, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра)',
                 #      '1', 'число', 8, card2),
                 ]
        res_str = '.дважды (число плюс слово) плюс слово'
        error = Errors()
        error.collision('число', ['один', '1'])
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # collision polytyped links neg test
    def test_32(self):
        card1 = Card('число', ['один', 'два'])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkFiniteFields('число', [8])
        vals_links1 = LinkFiniteFields('число', [0, 22])
        name_links2 = LinkFiniteFields('слово', [31, 19])
        vals_links2 = LinkFiniteFields('слово', [11, 33, 44])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)
        card2_link2 = TemplValLinkData(name_links2, vals_links2)

        card2.templates = [TemplValData('дважды (число плюс слово) плюс слово',
                                        'число плюс слово плюс число плюс слово плюс слово',
                                        [card2_link1, card2_link2])]
        inp_str = '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб'
        user_str = 'user_str'
        swaps = [Swap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                      '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                      'один', 'число', 1, card1),
                 Swap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                      '.число плюс слово плюс 1 плюс абракадабра плюс абракадаб', 'абракадабра',
                      'слово', 12, card3),
                 Swap('.число плюс слово плюс 1 плюс абракадабра плюс абракадаб',
                      '.число плюс слово плюс один плюс абракадабра плюс абракадаб',
                      '1', 'один', 23, card4),
                 Swap('.число плюс слово плюс один плюс абракадабра плюс абракадаб',
                      '.число плюс слово плюс число плюс абракадабра плюс абракадаб',
                      'один', 'число', 23, card1),
                 Swap('.число плюс слово плюс число плюс абракадабра плюс абракадаб',
                      '.число плюс слово плюс число плюс слово плюс абракадаб', 'абракадабра',
                      'слово', 34, card3),
                 Swap('.число плюс слово плюс число плюс слово плюс абракадаб',
                      '.число плюс слово плюс число плюс слово плюс слово', 'абракадаб',
                      'слово', 45, card3),

                 # templ_swap
                 Swap('.число плюс слово плюс число плюс слово плюс слово',
                      '.дважды (число плюс слово) плюс слово',
                      'число плюс слово плюс число плюс слово плюс слово',
                      'дважды (число плюс слово) плюс слово',
                      1, card2)

                 # reverse swaps
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (число плюс слово) плюс абракадабра',
                 #      'абракадабра', 'слово', 32, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра) плюс слово',
                 #      'абракадабра', 'слово', 19, card2),
                 # Swap('.дважды (число плюс слово) плюс слово',
                 #      '.дважды (1 плюс абракадабра)',
                 #      '1', 'число', 8, card2),
                 ]
        res_str = '.дважды (число плюс слово) плюс слово'
        error = Errors()
        error.collision('число', ['один', '1'])
        error.collision('слово', ['абракадабра', 'абракадабра', 'абракадаб'])
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() != res.get_fields()

    # selfref + temple test
    def test_4(self):
        card1 = Card('число', ['один', 'двадцать'])
        selfref_links1 = LinkFiniteFields('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]

        card2 = Card('дважды число', [])
        one_name_links = LinkFiniteFields('число', [7])
        one_vals_links = LinkFiniteFields('число', [0, 11])
        many_temp_links = TemplValLinkData(one_name_links, one_vals_links)
        card2.templates = [TemplValData('дважды число', 'число плюс число',
                                        [many_temp_links])]
        inp_str = '.(двадцать-один) плюс (двадцать-один).'
        user_str = 'user_str'
        swaps = [Swap('.(двадцать-один) плюс (двадцать-один).',
                      '.(число-один) плюс (двадцать-один).',
                      'двадцать', 'число', 2, card1),
                 Swap('.(число-один) плюс (двадцать-один).',
                      '.(число-число) плюс (двадцать-один).',
                      'один', 'число', 8, card1),
                 Swap('.(число-число) плюс (двадцать-один).',
                      '.(число-число) плюс (число-один).',
                      'двадцать', 'число', 21, card1),
                 Swap('.(число-число) плюс (число-один).',
                      '.(число-число) плюс (число-число).',
                      'один', 'число', 27, card1),
                 Swap('.(число-число) плюс (число-число).',
                      '.число плюс (число-число).',
                      '(число-число)', 'число', 1, card1),
                 Swap('.число плюс (число-число).',
                      '.число плюс число.',
                      '(число-число)', 'число', 12, card1),

                 # замены по шаблону
                 Swap('.число плюс число.',
                      '.дважды число.',
                      'число плюс число', 'дважды число', 1, card2),
                 ]
        # 'дважды число',
        # 'дважды двадцать один']
        res_str = '.дважды (двадцать-один).'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # 41 = selfref + temple test (poly_typed links)
    def test_41(self):
        card1 = Card('число', ['один', 'два'])
        selfref_links1 = LinkFiniteFields('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkFiniteFields('число', [8])
        vals_links1 = LinkFiniteFields('число', [0, 22])
        name_links2 = LinkFiniteFields('слово', [31, 19])
        vals_links2 = LinkFiniteFields('слово', [11, 33, 44])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)
        card2_link2 = TemplValLinkData(name_links2, vals_links2)

        card2.templates = [TemplValData('дважды (число плюс слово) плюс слово',
                                        'число плюс слово плюс число плюс слово плюс слово',
                                        [card2_link1, card2_link2])]

        # print(card1.get_fields())
        # print(card2.get_fields())
        # print(card3.get_fields())
        # print(card4.get_fields())

        inp_str = '.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [Swap('.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 2, card4),
                 Swap('.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 2, card1),
                 Swap('.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 8, card4),
                 Swap('.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 8, card1),
                 Swap('.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                      'абракадабра', 'слово', 20, card3),
                 Swap('.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 32, card4),
                 Swap('.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 32, card1),
                 Swap('.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                      '1', 'один', 38, card4),
                 Swap('.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                      'один', 'число', 38, card1),

                 Swap('.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                      'абракадабра', 'слово', 50, card3),
                 Swap('.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                      'абракадабра', 'слово', 61, card3),

                 # selfrefs_swaps
                 Swap('.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                      '.число плюс слово плюс (число-число) плюс слово плюс слово',
                      '(число-число)', 'число', 1, card1),
                 Swap('.число плюс слово плюс (число-число) плюс слово плюс слово',
                      '.число плюс слово плюс число плюс слово плюс слово',
                      '(число-число)', 'число', 23, card1),

                 # templ_swap
                 Swap('.число плюс слово плюс число плюс слово плюс слово',
                      '.дважды (число плюс слово) плюс слово',
                      'число плюс слово плюс число плюс слово плюс слово',
                      'дважды (число плюс слово) плюс слово',
                      1, card2)
                 ]
        res_str = '.дважды ((1-1) плюс абракадабра) плюс абракадабра'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    def test_42(self):
        card1 = Card('число', ['один', 'два'])
        selfref_links1 = LinkFiniteFields('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkFiniteFields('число', [8])
        vals_links1 = LinkFiniteFields('число', [0, 22])
        name_links2 = LinkFiniteFields('слово', [31, 19])
        vals_links2 = LinkFiniteFields('слово', [11, 33, 44])

        card2_link1 = TemplValLinkData(name_links1, vals_links1)
        card2_link2 = TemplValLinkData(name_links2, vals_links2)

        card2.templates = [TemplValData('дважды (число плюс слово) плюс слово',
                                        'число плюс слово плюс число плюс слово плюс слово',
                                        [card2_link1, card2_link2])]

        # print(card1.get_fields())
        # print(card2.get_fields())
        # print(card3.get_fields())
        # print(card4.get_fields())

        inp_str = '.(1-1) плюс абракадабра плюс (1-один) плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [Swap('.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 2, card4),
                 Swap('.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 2, card1),
                 Swap('.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 8, card4),
                 Swap('.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 8, card1),
                 Swap('.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                      'абракадабра', 'слово', 20, card3),
                 Swap('.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                      '1', 'один', 32, card4),
                 Swap('.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                      'один', 'число', 32, card1),
                 Swap('.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                      '1', 'один', 38, card4),
                 Swap('.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                      'один', 'число', 38, card1),

                 Swap('.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                      'абракадабра', 'слово', 50, card3),
                 Swap('.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                      '.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                      'абракадабра', 'слово', 61, card3),

                 # selfrefs_swaps
                 Swap('.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                      '.число плюс слово плюс (число-число) плюс слово плюс слово',
                      '(число-число)', 'число', 1, card1),
                 Swap('.число плюс слово плюс (число-число) плюс слово плюс слово',
                      '.число плюс слово плюс число плюс слово плюс слово',
                      '(число-число)', 'число', 23, card1),

                 # templ_swap
                 Swap('.число плюс слово плюс число плюс слово плюс слово',
                      '.дважды (число плюс слово) плюс слово',
                      'число плюс слово плюс число плюс слово плюс слово',
                      'дважды (число плюс слово) плюс слово',
                      1, card2)
                 ]
        res_str = '.дважды ((1-1) плюс абракадабра) плюс абракадабра'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # selfref + collision test
    def test_5(self):
        card1 = Card('число', ['один', 'два', 'число число'])
        card2 = Card('дважды число', ['число плюс число'])
        inp_str = 'один два плюс два один'
        swaps = ['один два плюс два один',
                 'число два плюс два один',
                 'число число плюс два один',
                 'число число плюс число один',
                 'число число плюс число число',
                 'число плюс число число',
                 'число плюс число',
                 'дважды число']
        res_str = 'число плюс число'  # в 5 тесте строка настраивается (тк не было успешной шаблонной замены)
        error = Errors()
        error.collision('число', 'один два', 'два один')
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

    # id-s test (pos)
    def test_6(self):
        card1 = Card('число', ['один', 'два', 'число число', 'число.число'])
        card2 = Card('число.два плюс число.один', ['число.один плюс число.два'])
        inp_str = 'один плюс два'
        swaps = ['один плюс два',
                 'число плюс два',
                 'число плюс число',
                 'два плюс один']
        res_str = 'два плюс один'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

    # selfref + id-s test
    def test_7(self):
        card1 = Card('число', ['один', 'два', 'число число', 'число.число'])
        card2 = Card('число.два плюс число.один', ['число.один плюс число.два'])
        inp_str = 'один плюс два один'
        error = Errors()
        error.no_errors()
        swaps = ['один плюс два один',
                 'число плюс два один',
                 'число плюс число один',
                 'число плюс число число',
                 'число плюс число',
                 'два один плюс один']
        res_str = 'два один плюс один'
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

    # id-. in inp_str (neg!)
    # должен работать априори при всех пред. успешно работающих тестах
    # Те тратить силы на его доработку по идее не надо (если все пойдет хорошо)
    def test_8(self):
        card1 = Card('число', ['один', 'два', 'число число', 'число.число'])
        card2 = Card('число.два плюс число.один', ['число.один плюс число.два'])
        inp_str = 'один.один плюс два'
        error = Errors()
        error.no_errors()
        swaps = ['один.один плюс два',
                 'число.один плюс два',
                 'число.число плюс два',
                 'число.число плюс число']
        res_str = 'число плюс число'  # настраивается! Не было замен по шаблону
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()


if __name__ == '__main__':
    Tests().run_all_tests()
