from typing import List
# from pprint import pprint


class OneTempLink:
    def __init__(self, the_link: str, pos: List[int]):
        self.the_link = the_link
        self.pos = pos

    def get_fields(self):
        return [self.the_link, self.pos]


class LinkTypeData:
    def __init__(self, name_links: OneTempLink, val_links: OneTempLink):
        self.name_links = name_links
        self.val_links = val_links

    def get_fields(self):
        return [
            [link for link in self.name_links.get_fields()],
            [link for link in self.val_links.get_fields()]
        ]


class TemplVal:
    def __init__(self, name: str, val: str, many_temp_links: List[LinkTypeData]):
        self.name = name
        self.val = val
        self.many_temp_links = many_temp_links

    def get_fields(self):
        return [self.name, self.val,
                [one_temp_link.get_fields() for one_temp_link in self.many_temp_links]
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
                self.selfrefs,

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

    def no_errors(self):
        self._errors = [self._no_errors]
        return self._errors

    def collision(self, link_name: str, link_val1: str, link_val2: str):
        self._errors += [
            'Коллизия! неясно, на что заменять ' + link_name + ' - на ' + link_val1 + ' или на ' + link_val2 + '']
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


class ResStrStruct:
    def __init__(self, first_str: str, last_successful: str, user_str: str):
        self.first_str = first_str
        self.last_successful = last_successful
        self.empty = ''
        self.user_str = user_str

    def get_fields(self):
        return [self.first_str,
                self.last_successful,
                self.empty,
                self.user_str]


class Result:
    def __init__(self, swaps: list[Swap], res_str: ResStrStruct, errors: Errors):
        self.swaps = swaps
        self.res_str = res_str
        self.errors = errors

    def get_fields(self):
        return [[swap.get_fields() for swap in self.swaps], self.res_str.get_fields(), self.errors.get_fields()]


class Parser:
    def __init__(self, cards: List[Card], inp_str: str):
        self._cards = cards
        self._first_str = inp_str
        self._user_str = None
        self._str = inp_str
        self._swaps = []
        self._errors = Errors()
        self._errors.no_errors()
        self._res = Result([], ResStrStruct('', '', ''), self._errors)

    def longest_of_nearest_val(self, inp_str: str, cards: List[Card]):
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

    def longest_of_nearest_templ(self, inp_str: str, cards: List[Card]):
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
                    for one_templ_link in one_template.many_temp_links:
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

    def _simple_swaps(self, longest_of_nearest):
        while True:
            # print(self._str)
            found_val = longest_of_nearest(self._str, self._cards)
            if found_val.get_fields() == Swap(self._str, '', '', '', 0, Card('', [])).get_fields():
                break
            else:
                self._str = self._str.replace(found_val.link_val, found_val.link_name, 1)
                self._swaps += [found_val]
                self._swaps[-1].cur_str = self._str
                # input()
        self._res = Result(self._swaps, ResStrStruct(self._first_str, self._str, self._user_str), self._errors)

    def _selfrefs_swaps(self):
        pass

    def _templates_swaps(self):
        # тут пригодился бы полиморфизм
        # шаблонные замены
        self._simple_swaps(self.longest_of_nearest_templ)
        # если замен по шаблону не произошло, строка настраивается
        pass

    def _get_used_templ(self, last_templ_swap: Swap) -> TemplVal:
        for one_swap in self._swaps[-2: 0: -1]:
            # перебираем все шаблоны
            for one_templ in last_templ_swap.card.templates:
                for one_link in one_templ.many_temp_links:
                    # print(one_link.get_fields())
                    # print(one_swap.link_name)
                    # print()
                    # ищем тот, который используется
                    if one_link.name_links.the_link == one_swap.link_name:
                        # print(one_templ.get_fields())
                        return one_templ
        # Если None - значит ни один шаблон не использовался в последней простой замене

    def _not_collision(self, used_templ: TemplVal):
        links_names = dict()
        for one_link in used_templ.many_temp_links:
            links_names[one_link.val_links.the_link] = [one_link.val_links.the_link]
        for one_swap in self._swaps[-2:: -1]:
            for one_link_name in links_names:
                for other_link_name in links_names[one_link_name]:
                    # ДОБАВИТЬ!! : сравнение по pos
                    # НЕТ!!! POS НЕ НУЖЕН! Все будет работать и без него
                    # (По крайней мере, до момента теста #21 включительно)
                    if one_swap.link_name == other_link_name:
                        links_names[one_link_name] += [one_swap.link_val]
        # print(links_names)
        links_res = {}
        for one_link_name in links_names:
            # В links_names[one_link_name] лежит имя ссылки (one_link.val_links.the_link), а после
            # все значения ссылки
            # При этом каждое значение ссылки - конечное.
            # То есть если есть разные концы (сначала отрезать имя в первой ячейке), КОЛЛИЗИЯ
            for other_link_name in links_names[one_link_name][2:]:
                if other_link_name != links_names[one_link_name][1]:
                    return [False, []]
                else:
                    links_res[one_link_name] = links_names[one_link_name][-1]
        # print(links_names)
        return [True, links_res]

    def get_reverse_links(self, reverse_links: TemplVal, collection_obj):
        # сортирует все pos в name_links
        # возвращает словарь, где левое поле - pos,
        # правое - список [что заменяли, на что заменяли]
        res = dict()
        # print(collection_obj)
        print(reverse_links.get_fields())
        for one_temp_link in reverse_links.many_temp_links:
            if one_temp_link.name_links.the_link in collection_obj.keys():
                for one_pos in one_temp_link.name_links.pos:
                    res[one_pos] = \
                        [one_temp_link.name_links.the_link,
                         collection_obj[one_temp_link.name_links.the_link]]
        # print(res)
        return res

    def _reverse_swaps(self):
        if self._swaps and self._swaps[len(self._swaps) - 1].card.templates != []:
            res_str = self._res.res_str.last_successful
            last_templ_swap = self._swaps[len(self._swaps) - 1]
            one_used_templ = self._get_used_templ(last_templ_swap)
            collection_obj = self._not_collision(one_used_templ)
            if collection_obj[0]:
                # print('YES!')
                reverse_links = self.get_reverse_links(one_used_templ, collection_obj[1])
                print(reverse_links)
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

    def start_warp_drive(self, user_str: str):
        self._user_str = user_str
        self._simple_swaps(self.longest_of_nearest_val)
        # self._selfrefs_swaps()
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

        # ДОБИТЬСЯ РАБОТЫ СЛЕД. ТЕСТА - КОЛЛИЗИИ!
        print('#3', self.test_3(), '\n')
        # print('#4', self.test_4(), '\n')
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
        one_name_links = OneTempLink('число', [7])
        one_vals_links = OneTempLink('число', [0, 11])
        many_temp_links = LinkTypeData(one_name_links, one_vals_links)
        user_str = 'user_str'
        card2.templates = [TemplVal('дважды число', 'число плюс число',
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
        name_links1 = OneTempLink('число', [8])
        vals_links1 = OneTempLink('число', [0, 22])
        name_links2 = OneTempLink('слово', [31, 19])
        vals_links2 = OneTempLink('слово', [11, 33, 44])

        card2_link1 = LinkTypeData(name_links1, vals_links1)
        card2_link2 = LinkTypeData(name_links2, vals_links2)

        card2.templates = [TemplVal('дважды (число плюс слово) плюс слово',
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
        return Parser([card1, card2, card3], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # collision test
    def test_3(self):
        card1 = Card('число', ['один', 'два'])
        # card2 = Card('дважды число', ['число плюс число'])
        card2 = Card('дважды число', [])

        name_links1 = OneTempLink('число', [7])
        vals_links1 = OneTempLink('число', [0, 11])

        card2_link1 = LinkTypeData(name_links1, vals_links1)

        card2.templates += [TemplVal('дважды число', 'число плюс число', [card2_link1])]

        inp_str = '.один плюс два.'
        user_str = 'user_str'
        swaps = [Swap('.один плюс два.', '.число плюс два.', 'один', 'число', 0, card1),
                 Swap('.число плюс один.', '.число плюс число.', 'два', 'число', 11, card1)
                 ]
        res_str = '.число плюс число.'  # в 3 тесте эта строка настраивается юзером!
        error = Errors()
        error.collision('число', 'один', 'два')
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # selfref + temple test
    def test_4(self):
        card1 = Card('число', ['один', 'двадцать', 'число число'])
        card2 = Card('дважды число', ['число плюс число'])
        inp_str = 'двадцать один плюс двадцать один'
        swaps = ['двадцать один плюс двадцать один',
                 'число один плюс двадцать один',
                 'число число плюс двадцать один',
                 'число число плюс число один',
                 'число число плюс число число',
                 'число плюс число число',
                 'число плюс число',
                 'дважды число',
                 'дважды двадцать один']
        res_str = 'дважды двадцать один'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

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
