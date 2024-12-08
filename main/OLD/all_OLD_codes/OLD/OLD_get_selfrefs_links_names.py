def get_selfrefs_links_names(self, links_names: dict, one_swap: Swap, i):
    # перебираем самоссылки (может быть одна)
    res_val = ''
    i_shift = 0
    for one_ref in one_swap.card.selfrefs:
        if one_swap.link_val == one_ref.the_link:
            i_shift += len(one_ref.positions) + 1
    print(i_shift)
    for one_ref in one_swap.card.selfrefs:
        if one_swap.link_val == one_ref.get_fields()[0]:
            res_val = one_ref.the_link[:one_ref.positions[0]]
            for j in range(len(one_ref.positions) - 1):
                cur_val = self._swaps[-i_shift - len(one_ref.positions) * (i + 1) + j].link_val
                res_val += cur_val
                res_val += one_ref.the_link[one_ref.positions[j] + len(one_swap.card.name):one_ref.positions[j + 1]]
            j = len(one_ref.positions) - 1
            cur_val = self._swaps[-i_shift - len(one_ref.positions) * (i + 1) + j].link_val
            res_val += cur_val
            res_val += one_ref.the_link[len(res_val):]
            # if res_val != '' and res_val not in links_names[one_swap.card.name]:
            links_names[one_swap.card.name] += [res_val]
    print(links_names)
    return links_names