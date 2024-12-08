def get_link_names(self, used_templ: TemplVal):
    links_names = dict()
    for one_link in used_templ.links:
        links_names[one_link.val_links.the_link] = [one_link.val_links.the_link]
    prev_links = -1
    i = 0
    while i < len(self._swaps[-2:: -1]):
        # for i, one_swap in enumerate(self._swaps[-2:: -1]):
        # Процедура сочленения значений столько раз,
        # сколько их есть в самоссылке
        one_swap = self._swaps[-2:: -1][i]
        if one_swap.card.selfrefs:  # != []
            # перебираем самоссылки (может быть одна)
            i_shift = 0
            for one_ref in one_swap.card.selfrefs:
                if one_swap.link_val == one_ref.get_fields()[0]:
                    i_shift += len(one_ref.positions) + 1
            for one_ref in one_swap.card.selfrefs:
                print(one_swap.link_val, '|', one_ref.get_fields()[0])
                if one_swap.link_val == one_ref.get_fields()[0]:
                    res_val = ''
                    for j in range(len(one_ref.positions) - 1):
                        cur_val = self._swaps[-i_shift - len(one_ref.positions) * (i + 1) + j].link_val
                        res_val += cur_val
                        res_val += one_ref.the_link[one_ref.positions[j] + len(one_swap.card.name):one_ref.positions[j + 1]]
                        # print(self._swaps[-i_shift-len(one_ref.pos)*(i+1)+j].link_val)
                        # print(one_ref.the_link, one_ref.pos[j], len(one_swap.card.name))
                        # print(i, j, self._swaps[-i_shift-len(one_ref.pos)*(i+1)+j].link_val)
                        # print(i, j, [other_swap.link_val for other_swap in self._swaps])
                    j = len(one_ref.positions) - 1
                    cur_val = self._swaps[-i_shift - len(one_ref.positions) * (i + 1) + j].link_val
                    res_val += cur_val
                    res_val += one_ref.the_link[len(res_val):]
                    # print(self._swaps[-i_shift - len(one_ref.pos) * (i + 1) + j].link_val)
                    # print(one_ref.the_link, one_ref.pos[j], len(one_swap.card.name))
                    # print(i, j, self._swaps[-i_shift - len(one_ref.pos) * (i + 1) + j].link_val)
                    # print(i, j, [other_swap.link_val for other_swap in self._swaps])
                    print(res_val)
                # и скипануть в цикле i_shift свапов
                # print(i_shift)
                # i += i_shift
        else:
            for one_link_name in links_names:
                for other_link_name in links_names[one_link_name]:
                    # если текущая позиция совпадает с последней,
                    # значит ссылка та же, но более глубокое значение
                    if one_swap.link_name == other_link_name:
                        if prev_links == one_swap.positions or \
                                False:
                            links_names[one_link_name].remove(one_swap.link_name)
                        links_names[one_link_name] += [one_swap.link_val]
            prev_links = one_swap.positions
        i += 1
    print(links_names)
    return links_names