def _get_templ_link_name_and_val_n(self, last_templ_swap: Swap):
    last_templ_links_in_name_n = 0
    last_templ_links_in_val_n = 0
    for one_template in last_templ_swap.card.templates:
        for one_link in one_template.links:
            last_templ_links_in_name_n += len(one_link.name_links.positions)
            last_templ_links_in_val_n += len(one_link.val_links.positions)
    return last_templ_links_in_name_n, last_templ_links_in_val_n