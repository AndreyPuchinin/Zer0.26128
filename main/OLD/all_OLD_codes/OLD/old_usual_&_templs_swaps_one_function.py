from typing import List


class Card:
    def __init__(self, name: str, vals: List[str]):
        self.name = name
        self.usual_vals = []
        self.selfrefs = []
        self.templates = []
        self.templ_refs = []
        for val in vals:
            self._check_and_classify_val(val)

    def _check_and_classify_val(self, val: str):
        # ВРЕМЕННО все значения = usual
        self.usual_vals += [val]

    def get_fields(self):
        return [self.name,
                self.usual_vals,
                self.selfrefs,
                self.templates,
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
        self._collision_error = 'Коллизия!'  # надо сделать это f()-ей с параметрами!!
        # ...
        pass

    def get_fields(self):
        return self._errors

    def no_errors(self):
        self._errors = [self._no_errors]
        return self._errors

    def collision(self, link: str, link_val1: str, link_val2: str):
        self._errors += [
            'Коллизия! неясно, на что заменять ' + link + ' - на ' + link_val1 + ' или на ' + link_val2 + '']
        return self._errors

    # def error_type_1(self):
    #     self.errors += [self.error_type_1]
    #     return self.errors


class Swap:
    def __init__(self, val, name, pos):
        self.val = val
        self.name = name
        self.pos = pos

    def get_fields(self):
        return [self.val, self.name, self.pos]


class Result:
    def __init__(self, swaps: list[Swap], res_str: str, errors: Errors):
        self.swaps = swaps
        self.res_str = res_str
        self.errors = errors

    def get_fields(self):
        return [[swap.get_fields() for swap in self.swaps], self.res_str, self.errors.get_fields()]


class Parser:
    class OneValTypeCard:
        def __init__(self, name: str, vals: List[str]):
            self.name = name
            self.vals = vals

        def _get_fields(self):
            return [self.name, self.vals]

    def UsualTypeCard(self) -> List[OneValTypeCard]:
        usual_type_cards = []
        usual_vals = []
        for card in self._cards:
            usual_vals += card.usual_vals
            one_usual_type_card = self.OneValTypeCard(card.name, usual_vals)
            usual_type_cards += [one_usual_type_card]
        return usual_type_cards

    def TemplTypeCard(self) -> List[OneValTypeCard]:
        templ_type_cards = []
        templ_vals = []
        for card in self._cards:
            templ_vals += [card.templates]
            one_templ_type_card = self.OneValTypeCard(card.name, templ_vals)
            templ_type_cards += [one_templ_type_card]
        return templ_type_cards

    def __init__(self, cards: List[Card], inp_str: str):
        self._cards = cards
        self._str = inp_str
        self._swaps = []
        self._errors = Errors()
        self._errors.no_errors()
        self._res = Result([], '', self._errors)

    def longest_of_nearest_val(self, inp_str: str, cards: List[OneValTypeCard]):
        # ищем самое длинное из всех самых близких вхождений
        # и формируем объект Swap
        # (см. в neuro_(...).py-файлах)

        longest_val = ""
        longest_name = ""
        longest_pos = 0

        j = 0
        for card in cards:
            print(j)
            print('name =', card.name)
            print('vals =', card.vals)
            j+=1
            for val in card.vals:
                for i in range(len(inp_str) - len(val) + 1):
                    if inp_str[i:i + len(val)] == val:
                        if len(val) > len(longest_val):
                            longest_val = val
                            longest_name = card.name
                            longest_pos = i
                            break
        return Swap(longest_val, longest_name, longest_pos)

    def _straight_swaps(self, one_type_cards):
        while True:
            found_val = self.longest_of_nearest_val(self._str, one_type_cards)
            if found_val.get_fields() == Swap('', '', 0).get_fields():
                break
            else:
                self._str = self._str.replace(found_val.val, found_val.name, 1)
                self._swaps += [found_val]
                # input()
        self._res = Result(self._swaps, self._str, self._errors)

    def _simple_swaps(self):
        self._straight_swaps(self.UsualTypeCard())
        pass

    def _selfrefs_swaps(self):
        pass

    def _templates_swaps(self):
        self._straight_swaps(self.TemplTypeCard())
        pass

    def _reverse_swaps(self):
        pass

    def start_warp_drive(self):
        self._simple_swaps()
        # self._selfrefs_swaps()
        self._templates_swaps()
        self._reverse_swaps()
        # errors = Errors()
        # errors.no_errors()
        # res = Result([], '1', errors)
        # res = Result([], self._str, errors)
        # print(res.get_fields())
        """ for card in self._cards:
            print('name =', card.name)
            print('templ =', card.templates)
        print(self._res.get_fields())
        print(self._str)"""
        return self._res


class Tests:
    def __init__(self):
        pass

    def run_all_tests(self):
        print('#0', self.test_0(), '\n')
        print('#1', self.test_1(), '\n')
        print('#11', self.test_11(), '\n')
        print('#2', self.test_2(), '\n')
        # print('#3', self.test_3(), '\n')
        # print('#4', self.test_4(), '\n')
        # print('#5', self.test_5(), '\n')
        # print('#6', self.test_6(), '\n')
        # print('#7', self.test_7(), '\n')
        # print('#8', self.test_8(), '\n')

    def test_0(self):
        card1 = Card('число', ['один'])
        inp_str = '1'
        swaps = []
        res_str = '1'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        return Parser([card1], inp_str).start_warp_drive().get_fields() == res.get_fields()

    def test_1(self):
        card1 = Card('число', ['один'])
        inp_str = 'один'
        swaps = [Swap('один', 'число', 0)]
        res_str = 'число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        return Parser([card1], inp_str).start_warp_drive().get_fields() == res.get_fields()

    def test_11(self):
        card1 = Card('число', ['один'])
        inp_str = 'один плюс один'
        swaps = [Swap('один', 'число', 0),
                 Swap('один', 'число', 11)]
        res_str = 'число плюс число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        return Parser([card1], inp_str).start_warp_drive().get_fields() == res.get_fields()

    def test_2(self):
        card1 = Card('число', ['один'])
        # card2 = Card('дважды число', ['число плюс число'])
        card2 = Card('дважды число', [])
        card2.templates = ['число плюс число']
        inp_str = 'один плюс один'
        swaps = [Swap('один', 'число', 0),
                 Swap('один', 'число', 11),
                 Swap('число плюс число', 'дважды число', 0),  # temple swap
                 Swap('число', 'один', 7)]  # reverse swap
        res_str = 'дважды один'
        error = Errors()
        error.no_errors()
        res = Result(swaps, res_str, error)
        # print(Parser([card1], inp_str).start_warp_drive().get_fields())
        # print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

    def test_3(self):
        card1 = Card('число', ['один', 'два'])
        # card2 = Card('дважды число', ['число плюс число'])
        card2 = Card('дважды число', [])
        card2.templates = ['число плюс число']
        inp_str = 'один плюс два'
        swaps = ['один плюс два',
                 'число плюс один',
                 'число плюс число']
        res_str = 'число плюс число'  # в 3 тесте эта строка настраивается юзером!
        error = Errors()
        error.collision('число', 'один', 'два')
        res = Result(swaps, res_str, error)
        return Parser([card1, card2], inp_str).start_warp_drive().get_fields() == res.get_fields()

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
