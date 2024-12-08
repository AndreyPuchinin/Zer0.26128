def get_links_to_reverse(self, last_templ_links_in_val_n: int):
    used_links = []
    for swap in self._swaps[-2: -2 - last_templ_links_in_val_n: -1]:
        # print(555)
        if not used_links:
            used_links += [[swap.link_val, swap.link_name]]
        print(used_links)
        link_was_used = False
        for one_used_link in used_links:
            if swap.link_val == one_used_link[0] and \
                    swap.link_name == one_used_link[1]:
                link_was_used = True
        if not link_was_used:
            used_links += [[swap.link_val, swap.link_name]]
        # print(swap.link_val, swap.link_name, swap.pos)
    # print(used_links)
    return used_links