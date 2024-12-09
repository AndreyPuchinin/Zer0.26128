from ZeroSubClasses import Errors, Result, ResStrStruct, Card, OneSwap, LinkData, Link, Template
from ZeroParser import Parser


class Tests:
    def __init__(self):
        pass

    def run_all_tests(self):
        print('#0', self.test_0(), '\n')

        print('#01', self.test_01(), '\n')
        print('#02', self.test_02(), '\n')
        print('#03', self.test_03(), '\n')

        print('#1', self.test_1(), '\n')
        print('#11', self.test_11(), '\n')

        print('#2', self.test_2(), '\n')

        # print('#21', self.test_21(), '\n')
        # print('#3', self.test_3(), '\n')
        # print('#31', self.test_31(), '\n')
        # print('#32', self.test_32(), '\n')
        # print('#4', self.test_4(), '\n')
        # print('#41', self.test_41(), '\n')
        # print('#42', self.test_42(), '\n')

        # print('#5', self.test_5(), '\n')

        # print('#6', self.test_6(), '\n')
        # print('#7', self.test_7(), '\n')
        # print('#8', self.test_8(), '\n')

    # Чисто проверяем, что тест запускается
    # (тест ничего не делает! - нет замен, список свапов пуст)
    def test_0(self):
        card1 = Card('число', ['один'], [], [])
        inp_str = '.1'
        user_str = 'user_str'
        swaps = [
                   # ПЕРВОЕ пробегание по строке:
                   # прямые простые замены:
                   # ПРОВЕРКА, что прямых простых замен не было:
                   # -не было
                   # ЗАВЕРШЕНИЕ формирования свапов
                ]
        res_str = '.1'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # Проверяем Parser._suitable_val_entry_in_str(...)
    def test_01(self):
        card1 = Card(' один два ', ['1', '12', '1235', '124', '234567', '345678'],
                     [], [])
        inp_str = '01234567'
        user_str = 'user_str'
        swaps = [
                  # ПЕРВОЕ пробегание по строке:

                  # прямые простые замены:
                  OneSwap('01234567', '0 один два 34567',
                          '12', ' один два ', 1, card1)
                  # ПРОВЕРКА, что прямых простых замен не было:
                  # -были

                  # прямые замены по самоссылкам:
                  # -пока не рассматриваются

                  # шаблонные замены:
                  # -нет

                  # ВТОРОЕ пробегание по строке:

                  # прямые простые замены:
                  # -нет

                  # ПРОВЕРКА, что прямых простых замен не было:
                  # -не было

                  # ЗАВЕРШЕНИЕ формирования свапов
            ]
        res_str = '0 один два 34567'
        error = Errors()
        error.no_errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # Чуть > сложная проверка Parser._suitable_val_entry_in_str(...)
    def test_02(self):
        card1 = Card(' три->семь ', ['1235', '124', '34567', '345678'], [], [])
        inp_str = '01234567'
        user_str = 'user_str'
        swaps = [OneSwap('01234567', '012 три->семь ', '34567', ' три->семь ', 3, card1)]
        res_str = '012 три->семь '
        error = Errors()
        error.no_errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # Еще чуть > сложная проверка Parser._suitable_val_entry_in_str(...)
    def test_03(self):
        card1 = Card(' один два ', ['12'], [], [])
        inp_str = '1312'
        user_str = 'user_str'
        swaps = [OneSwap('1312', '13 один два ', '12', ' один два ', 2, card1)]
        res_str = '13 один два '
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # одна обычная замена без шаблона
    def test_1(self):
        card1 = Card('число', ['один', '1'], [], [])
        inp_str = '.один'
        user_str = 'user_str'
        swaps = [OneSwap('.один', '.число', 'один', 'число', 1, card1)]
        res_str = '.число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # две обычные замены без шаблона
    def test_11(self):
        card1 = Card('число', ['один', 'два'], [], [])
        inp_str = '.один плюс один'
        user_str = 'user_str'
        swaps = [OneSwap('.один плюс один', '.число плюс один',
                         'один', 'число', 1, card1),
                 OneSwap('.число плюс один', '.число плюс число',
                         'один', 'число', 12, card1)]
        res_str = '.число плюс число'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # простейшая замена по шаблону (pos)
    def test_2(self):
        # Карта 1 = 'число' / 'один', 'два'
        card1 = Card('число', ['один', 'три'], [], [])

        # Карта 2 (шаблон!) = 'дважды число' / 'число плюс число'
        # Настраиваем шаблон:
        first_non_terminal_links = LinkData('число', [7])
        first_terminal_links = LinkData('число', [0, 11])
        some_templ_links = Link(first_non_terminal_links, first_terminal_links)

        card2_template = Template('дважды число', 'число плюс число',
                                  [some_templ_links])

        # Сохраняем в шаблон
        card2 = Card('дважды число', [], [], [card2_template])

        user_str = 'user_str'
        inp_str = '.один плюс один.'

        swaps = [OneSwap('.один плюс один.', '.число плюс один.',
                         'один', 'число', 1, card1),
                 OneSwap('.число плюс один.', '.число плюс число.',
                         'один', 'число', 12, card1),

                 # templ_swap
                 OneSwap('.число плюс число.', '.дважды число.',
                         'число плюс число', 'дважды число', 1, card2),

                 # reverse swaps
                 OneSwap('.дважды число.', '.дважды один.',
                         'число', 'один', 7, card2)
                 ]
        res_str = '.дважды один.'
        error = Errors()
        error.no_errors()
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # замена по шаблону с двумя типами ссылок (pos)
    def test_21(self):
        card1 = Card('число', ['один', 'три'], [], [])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'], [], [])
        card3 = Card('слово', ['абракадабра', 'абракадаб'], [], [])
        card2 = Card('дважды (число плюс слово) плюс слово', [], [], [])
        name_links1 = LinkData('число', [8])
        vals_links1 = LinkData('число', [0, 22])
        name_links2 = LinkData('слово', [31, 19])
        vals_links2 = LinkData('слово', [11, 33, 44])

        card2_link1 = Link(name_links1, vals_links1)
        card2_link2 = Link(name_links2, vals_links2)

        card2.templates = [Template('дважды (число плюс слово) плюс слово',
                                    'число плюс слово плюс число плюс слово плюс слово',
                                    [card2_link1, card2_link2])]
        inp_str = '.1 плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.'
        user_str = 'user_str'
        usual_swaps = [  # первый пробег по строке
            OneSwap('.1 плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.',
                    '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.',
                    '1', 'один', 1, card4),
            OneSwap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.',
                    '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.',
                    'один', 'число', 1, card1),
            OneSwap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра.',
                    '.число плюс слово плюс 1 плюс абракадабра плюс абракадабра.',
                    'абракадабра', 'слово', 12, card3),
            OneSwap('.число плюс слово плюс 1 плюс абракадабра плюс абракадабра.',
                    '.число плюс слово плюс один плюс абракадабра плюс абракадабра.',
                    '1', 'один', 23, card4),

            # второй пробег по строке!
            OneSwap('.число плюс слово плюс один плюс абракадабра плюс абракадабра.',
                    '.число плюс слово плюс число плюс абракадабра плюс абракадабра.',
                    'один', 'число', 23, card1),
            OneSwap('.число плюс слово плюс число плюс абракадабра плюс абракадабра.',
                    '.число плюс слово плюс число плюс слово плюс абракадабра.',
                    'абракадабра', 'слово', 34, card3),
            OneSwap('.число плюс слово плюс число плюс слово плюс абракадабра.',
                    '.число плюс слово плюс число плюс слово плюс слово.',
                    'абракадабра', 'слово', 45, card3)]
        selfrefs_swaps = []
        templ_swaps = [OneSwap('.число плюс слово плюс число плюс слово плюс слово.',
                               '.дважды (число плюс слово) плюс слово.',
                               'число плюс слово плюс число плюс слово плюс слово',
                               'дважды (число плюс слово) плюс слово',
                               1, card2)]
        reverse_swaps = [OneSwap('.дважды (число плюс слово) плюс слово.',
                                 '.дважды (один плюс слово) плюс слово.',
                                 'число', 'один', 9, card2),
                         OneSwap('.дважды (один плюс слово) плюс слово.',
                                 '.дважды (один плюс абракадабра) плюс слово.',
                                 'слово', 'абракадабра', 19, card2),
                         OneSwap('.дважды (один плюс абракадабра) плюс слово.',
                                 '.дважды (один плюс абракадабра) плюс абракадабра.',
                                 'слово', 'абракадабра', 37, card2),
                         OneSwap('.дважды (один плюс абракадабра) плюс абракадабра.',
                                 '.дважды (1 плюс абракадабра) плюс абракадабра.',
                                 'один', '1', 9, card2)]
        all_swaps = [usual_swaps, selfrefs_swaps, templ_swaps, reverse_swaps]
        res_str = '.дважды (1 плюс абракадабра) плюс абракадабра'
        error = Errors()
        error.no_errors()
        res = Result(all_swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2, card3, card4], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # коллизия с одним типом ссылки (pos)
    def test_3(self):
        card1 = Card('число', ['один', 'два'], [], [])
        # card2 = Card('дважды число', ['число плюс число'])
        card2 = Card('дважды число', [], [], [])

        name_links1 = LinkData('число', [7])
        vals_links1 = LinkData('число', [0, 11])

        card2_link1 = Link(name_links1, vals_links1)

        card2.templates += [Template('дважды число', 'число плюс число', [card2_link1])]

        inp_str = '.один плюс два.'
        user_str = 'user_str'
        swaps = [
            # прямые замены
            OneSwap('.один плюс два.', '.число плюс два.', 'один', 'число', 1, card1),
            OneSwap('.число плюс два.', '.число плюс число.', 'два', 'число', 12, card1),

            # шаблонные замены
            OneSwap('.число плюс число.', '.дважды число.', 'число плюс число', 'дважды число', 1, card2)
        ]
        res_str = '.дважды число.'  # в 3 тесте эта строка настраивается юзером!
        error = Errors()
        error.collision('число', ['один', 'два'])
        res = Result(swaps, ResStrStruct(inp_str, res_str, user_str), error)
        print(Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields())
        print(res.get_fields())
        return Parser([card1, card2], inp_str).start_warp_drive(user_str).get_fields() == res.get_fields()

    # коллизия с двумя типами ссылки (pos test)
    def test_31(self):
        card1 = Card('число', ['один', 'два'])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [], [], [])
        name_links1 = LinkData('число', [8])
        vals_links1 = LinkData('число', [0, 22])
        name_links2 = LinkData('слово', [31, 19])
        vals_links2 = LinkData('слово', [11, 33, 44])

        card2_link1 = Link(name_links1, vals_links1)
        card2_link2 = Link(name_links2, vals_links2)

        card2.templates = [Template('дважды (число плюс слово) плюс слово',
                                    'число плюс слово плюс число плюс слово плюс слово',
                                    [card2_link1, card2_link2])]

        inp_str = '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [OneSwap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                         '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                         'один', 'число', 1, card1),
                 OneSwap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадабра',
                         '.число плюс слово плюс 1 плюс абракадабра плюс абракадабра', 'абракадабра',
                         'слово', 12, card3),
                 OneSwap('.число плюс слово плюс 1 плюс абракадабра плюс абракадабра',
                         '.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                         '1', 'один', 23, card4),
                 OneSwap('.число плюс слово плюс один плюс абракадабра плюс абракадабра',
                         '.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                         'один', 'число', 23, card1),
                 OneSwap('.число плюс слово плюс число плюс абракадабра плюс абракадабра',
                         '.число плюс слово плюс число плюс слово плюс абракадабра', 'абракадабра',
                         'слово', 34, card3),
                 OneSwap('.число плюс слово плюс число плюс слово плюс абракадабра',
                         '.число плюс слово плюс число плюс слово плюс слово', 'абракадабра',
                         'слово', 45, card3),

                 # templ_swap
                 OneSwap('.число плюс слово плюс число плюс слово плюс слово',
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

    # коллизия с двумя типами ссылки (neg test)
    def test_32(self):
        card1 = Card('число', ['один', 'два'])
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkData('число', [8])
        vals_links1 = LinkData('число', [0, 22])
        name_links2 = LinkData('слово', [31, 19])
        vals_links2 = LinkData('слово', [11, 33, 44])

        card2_link1 = Link(name_links1, vals_links1)
        card2_link2 = Link(name_links2, vals_links2)

        card2.templates = [Template('дважды (число плюс слово) плюс слово',
                                    'число плюс слово плюс число плюс слово плюс слово',
                                    [card2_link1, card2_link2])]

        inp_str = '.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб'
        user_str = 'user_str'
        swaps = [OneSwap('.один плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                         '.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                         'один', 'число', 1, card1),
                 OneSwap('.число плюс абракадабра плюс 1 плюс абракадабра плюс абракадаб',
                         '.число плюс слово плюс 1 плюс абракадабра плюс абракадаб', 'абракадабра',
                         'слово', 12, card3),
                 OneSwap('.число плюс слово плюс 1 плюс абракадабра плюс абракадаб',
                         '.число плюс слово плюс один плюс абракадабра плюс абракадаб',
                         '1', 'один', 23, card4),
                 OneSwap('.число плюс слово плюс один плюс абракадабра плюс абракадаб',
                         '.число плюс слово плюс число плюс абракадабра плюс абракадаб',
                         'один', 'число', 23, card1),
                 OneSwap('.число плюс слово плюс число плюс абракадабра плюс абракадаб',
                         '.число плюс слово плюс число плюс слово плюс абракадаб', 'абракадабра',
                         'слово', 34, card3),
                 OneSwap('.число плюс слово плюс число плюс слово плюс абракадаб',
                         '.число плюс слово плюс число плюс слово плюс слово', 'абракадаб',
                         'слово', 45, card3),

                 # templ_swap
                 OneSwap('.число плюс слово плюс число плюс слово плюс слово',
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

    # самоссылка + шаблон
    # selfref + temple test
    def test_4(self):
        card1 = Card('число', ['один', 'двадцать'])
        selfref_links1 = LinkData('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]

        card2 = Card('дважды число', [])
        one_name_links = LinkData('число', [7])
        one_vals_links = LinkData('число', [0, 11])
        many_temp_links = Link(one_name_links, one_vals_links)
        card2.templates = [Template('дважды число', 'число плюс число',
                                    [many_temp_links])]

        inp_str = '.(двадцать-один) плюс (двадцать-один).'
        user_str = 'user_str'
        swaps = [OneSwap('.(двадцать-один) плюс (двадцать-один).',
                         '.(число-один) плюс (двадцать-один).',
                         'двадцать', 'число', 2, card1),
                 OneSwap('.(число-один) плюс (двадцать-один).',
                         '.(число-число) плюс (двадцать-один).',
                         'один', 'число', 8, card1),
                 OneSwap('.(число-число) плюс (двадцать-один).',
                         '.(число-число) плюс (число-один).',
                         'двадцать', 'число', 21, card1),
                 OneSwap('.(число-число) плюс (число-один).',
                         '.(число-число) плюс (число-число).',
                         'один', 'число', 27, card1),
                 OneSwap('.(число-число) плюс (число-число).',
                         '.число плюс (число-число).',
                         '(число-число)', 'число', 1, card1),
                 OneSwap('.число плюс (число-число).',
                         '.число плюс число.',
                         '(число-число)', 'число', 12, card1),

                 # замены по шаблону
                 OneSwap('.число плюс число.',
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

    # самоссылка (selfref) + шаблон с двумя типами ссылки
    def test_41(self):
        card1 = Card('число', ['один', 'два'])
        selfref_links1 = LinkData('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkData('число', [8])
        vals_links1 = LinkData('число', [0, 22])
        name_links2 = LinkData('слово', [31, 19])
        vals_links2 = LinkData('слово', [11, 33, 44])

        card2_link1 = Link(name_links1, vals_links1)
        card2_link2 = Link(name_links2, vals_links2)

        card2.templates = [Template('дважды (число плюс слово) плюс слово',
                                    'число плюс слово плюс число плюс слово плюс слово',
                                    [card2_link1, card2_link2])]

        # print(card1.get_fields())
        # print(card2.get_fields())
        # print(card3.get_fields())
        # print(card4.get_fields())

        inp_str = '.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [OneSwap('.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 2, card4),
                 OneSwap('.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 2, card1),
                 OneSwap('.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 8, card4),
                 OneSwap('.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 8, card1),
                 OneSwap('.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                         'абракадабра', 'слово', 20, card3),
                 OneSwap('.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 32, card4),
                 OneSwap('.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 32, card1),
                 OneSwap('.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                         '1', 'один', 38, card4),
                 OneSwap('.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                         'один', 'число', 38, card1),

                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                         'абракадабра', 'слово', 50, card3),
                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                         'абракадабра', 'слово', 61, card3),

                 # selfrefs_swaps
                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                         '.число плюс слово плюс (число-число) плюс слово плюс слово',
                         '(число-число)', 'число', 1, card1),
                 OneSwap('.число плюс слово плюс (число-число) плюс слово плюс слово',
                         '.число плюс слово плюс число плюс слово плюс слово',
                         '(число-число)', 'число', 23, card1),

                 # templ_swap
                 OneSwap('.число плюс слово плюс число плюс слово плюс слово',
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

    # самоссылки (selfref) с разной степенью глубины +
    # + шаблон (templ) с двумя типами ссылки, (~neg!~)
    def test_42(self):
        card1 = Card('число', ['один', 'два'])
        selfref_links1 = LinkData('(число-число)', [1, 7])
        card1.selfrefs = [selfref_links1]
        # ДОПОЛНИТЬ В SWAPS ЗАМЕНУ 1 -> один -> число
        card4 = Card('один', ['1'])
        card3 = Card('слово', ['абракадабра', 'абракадаб'])
        card2 = Card('дважды (число плюс слово) плюс слово', [])
        name_links1 = LinkData('число', [8])
        vals_links1 = LinkData('число', [0, 22])
        name_links2 = LinkData('слово', [31, 19])
        vals_links2 = LinkData('слово', [11, 33, 44])

        card2_link1 = Link(name_links1, vals_links1)
        card2_link2 = Link(name_links2, vals_links2)

        card2.templates = [Template('дважды (число плюс слово) плюс слово',
                                    'число плюс слово плюс число плюс слово плюс слово',
                                    [card2_link1, card2_link2])]

        # print(card1.get_fields())
        # print(card2.get_fields())
        # print(card3.get_fields())
        # print(card4.get_fields())

        inp_str = '.(1-1) плюс абракадабра плюс (1-один) плюс абракадабра плюс абракадабра'
        user_str = 'user_str'
        swaps = [OneSwap('.(1-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 2, card4),
                 OneSwap('.(один-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 2, card1),
                 OneSwap('.(число-1) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 8, card4),
                 OneSwap('.(число-один) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 8, card1),
                 OneSwap('.(число-число) плюс абракадабра плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                         'абракадабра', 'слово', 20, card3),
                 OneSwap('.(число-число) плюс слово плюс (1-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                         '1', 'один', 32, card4),
                 OneSwap('.(число-число) плюс слово плюс (один-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                         'один', 'число', 32, card1),
                 OneSwap('.(число-число) плюс слово плюс (число-1) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                         '1', 'один', 38, card4),
                 OneSwap('.(число-число) плюс слово плюс (число-один) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                         'один', 'число', 38, card1),

                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс абракадабра плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                         'абракадабра', 'слово', 50, card3),
                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс слово плюс абракадабра',
                         '.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                         'абракадабра', 'слово', 61, card3),

                 # selfrefs_swaps
                 OneSwap('.(число-число) плюс слово плюс (число-число) плюс слово плюс слово',
                         '.число плюс слово плюс (число-число) плюс слово плюс слово',
                         '(число-число)', 'число', 1, card1),
                 OneSwap('.число плюс слово плюс (число-число) плюс слово плюс слово',
                         '.число плюс слово плюс число плюс слово плюс слово',
                         '(число-число)', 'число', 23, card1),

                 # templ_swap
                 OneSwap('.число плюс слово плюс число плюс слово плюс слово',
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

    # самоссылка (selfref) + коллизия (collision)
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

    # идентификаторы (id-s), (pos)
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

    # самоссылки (selfref) + идентификаторы (id-s)
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

    # нетерминал идентификатора внутри входной строки (neg!)
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
