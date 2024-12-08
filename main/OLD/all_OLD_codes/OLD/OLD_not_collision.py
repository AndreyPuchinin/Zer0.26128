def _not_collision(self,
                   used_templ: OneTempLink):  # link_name: str, pos: int, last_templ_links_in_val_n: int, last_templ_swap: Swap):
    for one_link in used_templ.links:
        # print(one_link.get_fields())
        print(self._link_source(self._swaps[-2: 0: -1], one_link.val_links.the_link, one_link.val_links.positions))
    # for i in range(len(used_links)):
    # print(self._link_source(self._swaps[-2: 0: -1], used_links[i]))
    # print()
    # used_links = []
    # for one_templ in last_templ_swap.card.templates:
    #     for one_link in one_templ.many_temp_links:
    #         print(link_name, one_link.get_fields())
    #         print(pos, last_templ_swap.get_fields())
    #         if link_name == one_link.val_links.the_link and \
    #                 pos - last_templ_swap.pos in one_link.val_links.pos:
    #             # print(link_name, one_link.get_fields())
    #             used_links += [one_link]
    # return self._all_links_vals_eq(used_links, last_templ_links_in_val_n)