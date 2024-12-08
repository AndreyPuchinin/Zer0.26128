def _not_collision(self, used_templ: TemplVal):
    links_data = SelfrefLinksData(self.get_selfrefs_links_one_name,
                                  self._link_name_reverse)
    links_data.get_links_data(used_templ, self._swaps)
    # print(links_data.get_fields())
    # print(links_data)
    links_res = {}
    caught_error = False
    caught_error_links_names = []
    for one_link_name in links_data.get_fields():
        # print(one_link_name)
        # В links_data[one_link_name] лежит имя ссылки (one_link.val_links.the_link), а после
        # все значения ссылки
        # Иначе (если первый элемент другой) не работает цикл выше (теперь get_link_names),
        # (не выполняет то, что должно)
        # При этом каждое значение ссылки - конечное.
        # То есть если есть разные концы (сначала отрезать имя в первой ячейке), КОЛЛИЗИЯ
        for other_link_name in links_data.get_fields()[one_link_name][1:]:
            # Проверка на коллизию:
            # Если да,
            # то сразу накапливаем ошибку в self._res.errors!
            if other_link_name != links_data.get_fields()[one_link_name][0] and \
                    one_link_name not in caught_error_links_names:
                caught_error = True
                error_names = links_data.get_fields()[one_link_name].copy()
                error_names.reverse()
                # print(error_names)
                error_names_without_doubles = []
                for one_error_name in error_names:
                    if one_error_name not in error_names_without_doubles:
                        error_names_without_doubles.append(one_error_name)
                # print(error_names_without_doubles)
                self._res.errors.collision(one_link_name, error_names_without_doubles)
                caught_error_links_names += [one_link_name]
            else:
                links_res[one_link_name] = links_data.get_fields()[one_link_name][-1]
    if not caught_error:
        print([True, links_res])
        return [True, links_res]
    else:
        print([False, {}])
        return [False, {'a': 1}]