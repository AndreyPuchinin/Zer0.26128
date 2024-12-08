from typing import List
from abc import ABC, abstractmethod

class ZeroEntity(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_fields(self) -> list:
        pass


"""V - ЗАМЕНИТЬ ИМЯ И ЗНАЧЕНИЕ НА ТЕРМИНАЛ И НЕТЕРМИНАЛ!!! - 
       ЭТО РЕШИТ ПРОБЛЕМУ СОВПАДЕНИЯ ПОНЯТИЙ 'ЗНАЧЕНИЯ'"""


class LinkData(ZeroEntity):
    """Конечные поля ссылки (link): \n
       1.строка (будь то терминал или нетерминал шаблона или самоссылки) \n
       2.список позиций вхождений в терминал или нетерминал шаблона или самоссылки"""

    def __init__(self, the_link: str, positions: List[int]) -> None:
        """Устанавливает и хранит поля ссылки (link): \n
           1.строку (будь то терминал или нетерминал шаблона или самоссылки), \n
           2.а также все позиции вхождения данной строки в терминал или нетерминал шаблона или самоссылки"""
        self.the_link = the_link
        self.positions = positions

    def get_fields(self) -> list:
        """Вернет списком \n
           1.строку (будь то терминал или нетерминал шаблона или самоссылки), \n
           2.а также все позиции вхождения данной строки в терминал или нетерминал шаблона или самоссылки"""
        return [self.the_link, self.positions]


class Link(ZeroEntity):
    """Шаблонная ссылка (template link) или ссылка самоссылки (selfref link): \n
       ПОЛЯ (2): \n
       1.терминалы (значения), \n
       2.нетерминал (имя). \n
       (Оба поля является объектами LinkData)"""

    def __init__(self, non_terminals: LinkData, terminals: LinkData) -> None:
        """Устанавливает и хранит 2 ПОЛЯ: \n
           1.терминалы (значения) \n
           2.нетерминал (имя) \n
           шаблонной ссылки (template link) \n
           или \n
           ссылки самоссылки (selfref link). \n
           (Оба поля являются объектами LinkData)"""
        self.non_terminal = non_terminals
        self.terminal = terminals

    def get_fields(self) -> list:
        """Вернет список из подсписков - \n
           полей шаблонной ссылки (template link) \n
           или \n
           ссылки самоссылки (selfref link) \n
           (В обоих случаях поля являются объектами LinkData)"""
        return [
            [link for link in self.non_terminal.get_fields()],
            [link for link in self.terminal.get_fields()]
        ]


class Template(ZeroEntity):
    """Шаблонное значение: \n
       ПОЛЯ (3): \n
       1.строка имени, \n
       2.строка шаблонного значения,
       3.информация о ссылках (объекты класса Link) внутри шаблонного значения"""

    def __init__(self, name: str, val: str, links: List[Link]) -> None:
        """Устанавливает и хранит 3 поля: \n
           1.строку имени, \n
           2.строку шаблонного значения, \n
           3.информацию о ссылках (объекты класса Link) внутри шаблонного значения"""
        self.name = name
        self.val = val
        self.links = links

    def get_fields(self) -> list:
        """Вернет списком 3 поля: \n
           1.строку имени, \n
           2.строку шаблонного значения, \n
           3.информацию о ссылках (объекты класса Link) внутри шаблонного значения"""
        return [self.name, self.val,
                [one_link.get_fields() for one_link in self.links]
                ]


class SelfRef(ZeroEntity):
    """Значение-самоссылка: \n
       ПОЛЯ (3): \n
       1.строка имени, \n
       2.строка значения-самоссылки,
       3.информация о ссылках (объекты класса Link) внутри значения-самоссылки"""

    def __init__(self, name: str, vals: List[str], links: List[Link]) -> None:
        """Устанавливает и хранит 3 поля: \n
           1.строку имени, \n
           2.строку значения-самоссылки \n
           3.информацию о ссылках (объекты класса Link) внутри значения-самоссылки"""
        self.name = name
        self.vals = vals
        self.links = links

    def get_fields(self) -> list:
        """Вернет списком 3 поля: \n
           1.строку имени, \n
           2.строку значения-самоссылки \n
           3.информацию о ссылках (объекты класса Link) внутри значения-самоссылки"""
        return [self.name, self.vals,
                [one_link.get_fields() for one_link in self.links]
                ]


class Card(ZeroEntity):
    """Класс Карточки \n
       ПОЛЯ (4 или 5): \n
       1.имя карточки, \n
       2.обычные значения карточки, \n
       3.значения-самоссылки, \n
       4.шаблонные значения, \n
       (+5.значения, одновременно шаблонные и самоссылки. \n
           Эти значения можно попытаться исключить из кода, \n
           запустив алгоритм для одного значения такого типа \n
           сперва для самоссылок, \n
           а затем для шаблонов)"""

    def __init__(self, name: str, usual_vals: List[str], selfrefs: List[SelfRef],
                 templates: List[Template]) -> None:  # templ_refs) -> None:
        """Устанавливает и хранит 4 (или 5) полей: \n
           1.имя карточки, \n
           2.обычные значения карточки, \n
           3.значения-самоссылки, \n
           4.шаблонные значения, \n
           (+5.значения, одновременно шаблонные и самоссылки. \n
               Эти значения можно попытаться исключить из кода, \n
               запустив алгоритм для одного значения такого типа \n
               сперва для самоссылок, \n
               а затем для шаблонов)"""
        self.name = name
        self.usual_vals = usual_vals
        self.selfrefs = selfrefs
        self.templates = templates
        # self.templ_refs = []  # по идее можно дополнить в selfrefs, а потом в templates

    def get_fields(self) -> list:
        """Вернет списком 4 (или 5) полей: \n
           1.имя карточки, \n
           2.обычные значения карточки, \n
           3.значения-самоссылки, \n
           4.шаблонные значения, \n
           (+5.значения, одновременно шаблонные и самоссылки. \n
               Эти значения можно попытаться исключить из кода, \n
               запустив алгоритм для одного значения такого типа \n
               сперва для самоссылок,  \n
               а затем для шаблонов)"""
        return [self.name,
                self.usual_vals,
                [selfrefs.get_fields() for selfrefs in self.selfrefs],
                [template.get_fields() for template in self.templates],
                # self.templ_refs
                ]


class Errors(ZeroEntity):
    """Класс ошибки. \n
       ПОЛЯ (пока 2): \n
       1.Накопленные ошибки \n
       \n
       КОНСТАНТЫ (пока 1): \n
       2.1 БЕЗ ОШИБОК \n
       \n
       ПРОЧИЕ КОНСТАНТЫ ФОРМИРУЮТСЯ ПАРАМЕТРИЗИРУЕМЫМИ МЕТОДАМИ"""

    def __init__(self):
        """Устанавливает и хранит (пока) 2 поля:\n
           1.Накопленные ошибки \n
           \n
           КОНСТАНТЫ (пока 1): \n
           2.1 'БЕЗ ОШИБОК' \n
           \n
           ПРОЧИЕ КОНСТАНТЫ ФОРМИРУЮТСЯ ПАРАМЕТРИЗИРУЕМЫМИ МЕТОДАМИ"""
        self._errors = []

        self._no_errors = 'Успешно, ошибок нет!'
        # ...
        pass

    def get_fields(self):
        """Вернет списком 1-но поле \n
           (...И ЭТО РАБОЧИЙ ВАРИАНТ КОДА!!!): \n
           1.накопленные ошибки"""
        return self._errors

    def no_errors(self):
        """Сброс накапливания ошибок в 0. \n
           Положит в поле накопленных ошибок ТОЛЬКО константу \n
           'БЕЗ ОШИБОК'"""
        self._errors = [self._no_errors]
        return self._errors

    def errors_caught(self):
        """Удаление константы 'БЕЗ ОШИБОК' из накопленных ошибок. \n
           ВЫЗЫВАТЬ ИЗ КАЖДОГО МЕТОДА класса Errors, \n
           ГДЕ КОПИТСЯ ОШИБКА!!!"""
        while self._no_errors in self._errors:
            self._errors.remove(self._no_errors)

    def collision(self, terminal: str, non_terminals: List[str]):
        """Дополнит в поле накопленных ошибок строку о коллизии. \n
           \n
           ПАРАМЕТРЫ (2): \n
            \n
           1.нетерминал \n
           (имя шаблонной ссылки (template link) \n
           или \n
           ссылки самоссылки (selfref link)) \n
           \n
           2.терминалы \n
           (значения шаблонной ссылки (template link) \n
           или \n
           ссылки самоссылки (selfref link))"""
        self.errors_caught()
        res_str = 'Коллизия! Неясно, на что заменять \'' + terminal + '\' - на \'' + non_terminals[0] + '\''
        for one_link_val in non_terminals[1:-1]:
            res_str += ', \'' + one_link_val + '\''
        res_str += ' или \'' + non_terminals[-1] + '\''
        self._errors += [res_str]
        return self._errors


class OneSwap(ZeroEntity):
    """Класс замены. \n
       ПОЛЯ (6): \n
       1. Последняя версия строки \n
       2. Новая версия строки \n
       3. Что заменяем \n
       4. На что заменяем \n
       5. Позиция замены в строке (хоть в старой, хоть в новой - они =ы) \n
       6. Карточка, которая применяется для замены"""

    def __init__(self, prev_str: str, new_str: str, replaceable, replacing, pos, card: Card):
        """Устанавливает и хранит 6 полей: \n
           1. Последняя версия строки \n
           2. Новая версия строки \n
           3. Что заменяем \n
           4. На что заменяем \n
           5. Позиция замены в строке (хоть в старой, хоть в новой - они =ы) \n
           6. Карточка, которая применяется для замены"""
        self.prev_str = prev_str
        self.new_str = new_str
        self.replaceable = replaceable
        self.replacing = replacing
        self.pos = pos
        self.card = card

    def get_fields(self):
        """Вернет списком 6 полей: \n
           1.Последняя версия строки \n
           2.Новая версия строки \n
           3.Что заменяем \n
           4.На что заменяем \n
           5.Позиция замены в строке (хоть в старой, хоть в новой - они =ы) \n
           6.Карточка, которая применяется для замены"""
        return [self.prev_str,
                self.new_str,
                self.replaceable,
                self.replacing,
                self.pos,
                self.card.get_fields()]


class ResStrStruct(ZeroEntity):
    """Структура результирующих строк \n
       ПОЛЯ (3): \n
       1.первая строка, \n
       2.последняя успешная строка \n
       3.пользовательская настраиваемая строка"""

    def __init__(self, first_str: str, last_successful: str, user_str: str):
        """Устанавливает и хранит 3 поля: \n
           1.первая строка, \n
           2.последняя успешная строка \n
           3.пользовательская настраиваемая строка"""
        self.first_str = first_str
        self.last_successful = last_successful
        # self.empty = ''
        self.user_str = user_str

    def get_fields(self):
        """Вернет списком 3 поля: \n
           1.первая строка, \n
           2.последняя успешная строка \n
           3.пользовательская настраиваемая строка"""
        return [self.first_str,
                self.last_successful,
                # self.empty,
                self.user_str]


class Result(ZeroEntity):
    """Класс для проверки предполагаемого результата ПАРСИНГА \n
       ПОЛЯ (3): \n
       1. Свапы, \n
       2. 3 строки (класс ResStrStruct выше) \n
       3. ошибки"""

    def __init__(self, swaps: list[OneSwap], res_str: ResStrStruct, errors: Errors):
        """Устанавливает и хранит 3 поля: \n
           1. Свапы, \n
           2. 3 строки (класс ResStrStruct выше) \n
           3. ошибки"""
        self.swaps = swaps
        self.res_str = res_str
        self.errors = errors

    def get_fields(self):
        """Вернет списком 3 поля: \n
           1. Свапы, \n
           2. 3 строки (класс ResStrStruct выше) \n
           3. ошибки"""
        return [
            [swap.get_fields() for swap in self.swaps],
            self.res_str.get_fields(),
            self.errors.get_fields()
        ]
