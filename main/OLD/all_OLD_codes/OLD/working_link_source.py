def _link_source(self, swaps: List[Swap], one_used_link: str, pos: int):
    # Вытянуть из reverse_swaps_problem_solution.txt
    # Слово -> абракадабра
    # Число -> один -> 1
    # print('start')
    # for _one_swap in swaps:
    #     print(_one_swap.get_fields()[2:5])
    # print('cycle:')
    cur_name = one_used_link
    cur_pos = pos
    cur_val = None
    for i, one_swap in enumerate(swaps):
        # print(cur_name, one_swap.link_name)
        # print(cur_pos, one_swap.pos)
        if cur_name == one_swap.link_name:  # and \
            # print(cur_pos, one_swap.pos)
            cur_name = one_swap.link_val
            cur_val = one_swap.link_val
            # print(f'{cur_name = }')
            source = self._link_source(swaps[2:], cur_name, cur_pos)
            # print(1, cur_val)
            # print(2, source)
            if source:
                return source
            else:
                return cur_val
    return cur_val