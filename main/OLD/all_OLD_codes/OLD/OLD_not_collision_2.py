def _not_collision(self, used_templ: TemplVal):
    links_names = dict()
    for one_link in used_templ.links:
        links_names[one_link.val_links.the_link] = [one_link.val_links.the_link]
        # print(one_link.get_fields())
    for one_swap in self._swaps[-2:: -1]:
        for one_link_name in links_names:
            print(one_swap.cur_str[:one_swap.positions] + '| ' + one_swap.cur_str[one_swap.positions:])
            print(one_swap.link_name)
            print(links_names[one_link_name])
            # ДОБАВИТЬ!! : сравнение по pos
            if one_swap.link_name == one_link_name:
                print('YES!')
                links_names[one_link_name] += [one_swap.link_val]
                print(links_names)
            print()
    print(links_names)