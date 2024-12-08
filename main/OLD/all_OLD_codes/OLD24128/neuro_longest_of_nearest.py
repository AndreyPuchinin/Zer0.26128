from typing import List


class Card:
    def __init__(self, name: str, vals: List[str]):
        self.name = name
        self.vals = vals

    def show(self):
        return [self.name, self.vals]


cards = []
for i in range(5):
    card1 = Card(str(i + 1), ['a' * (i + 1)])
    cards += [card1]

inp_str = 's' + ('a' * 4)
print(inp_str)
for i in range(5):
    print(cards[i].show())


class Swap:
    def __init__(self, val, name, pos):
        self.val = val
        self.name = name
        self.pos = pos

    def get_fields(self):
        return [self.val, self.name, self.pos]


def longest_of_nearest_val(inp_str: str, cards: List[Card]) -> Swap:
    # реализуй функцию,
    # ищущую самое длинное из всех самых близких значений всех карт (Card)
    # формирующую объект Swap из найденного значения, имени подходящей карты и позиции вхождения значения в строку
    # и возвращающую объект Swap
    # для данной версии программы ответ должен совпадать с Swap('aaaa', '4', 1)
    longest_val = ""
    longest_name = ""
    longest_pos = 0

    for card in cards:
        for val in card.vals:
            for i in range(len(inp_str) - len(val) + 1):
                if inp_str[i:i + len(val)] == val:
                    if len(val) > len(longest_val):
                        longest_val = val
                        longest_name = card.name
                        longest_pos = i
                        break
    return Swap(longest_val, longest_name, longest_pos)


print(longest_of_nearest_val(inp_str, cards).get_fields())