def _reverse_swaps(self):
    if self._swaps:
        # надо ли сейчас?..
        last_templ_swap = self._swaps[len(self._swaps) - 1]
        templ_pos = last_templ_swap.positions

        # ПРОВЕРИТЬ ВСЕ ССЫЛКИ ШАБЛОНА

        # Находим общее число ссылок всех типов,
        # как в имени шаблона, так и в значении
        # (для итерирования в цикле по пред. свапам)
        last_templ_links_in_name_n, last_templ_links_in_val_n = \
            self._get_templ_link_name_and_val_n(last_templ_swap)

        print(self.get_links_to_reverse(last_templ_links_in_val_n))
        # for i in range(last_templ_links_in_name_n):
        # if not self._not_collision(self._swaps[i].link_name,
        #                            self._swaps[i].pos, last_templ_links_in_val_n,
        #                            last_templ_swap):
        # ...КОЛЛИЗИЯ
        print('&&&')
        # КОЛЛИЗИЯ - дополнить много значений в ошибку!!
        # self._res.errors.collision(last_templ_swap.link_name,
        #                           last_templ_swap.link_val,
        #                           templ_link_source_swap.link_val)
        # !!! return ... (res)

        # ЕСЛИ КОЛЛИЗИЯ НЕ ПРЕРВАЛА ВЫПОЛНЕНИЕ, ТО:
        # заменяем все ссылки на значения
        # реформируем res
        # swapped_times = 0
        # перебираем все свапы ПЕРЕД шаблонным столько раз, сколько ссылок всех типов в общем было в строке

        # !! Заменить каждую ссылку каждого типа !!
        # ищем шаблон для замены текущей ссылки
        # АЛГ ниже НЕОПТИМАЛЕН!!!
        # ++ если замена по этому шаблону уже была - можно пропустить!
        # Сейчас алг откатывается не по шаблону - а по свапам (подыскивая подходящий шаблон)
        # _cur_link = TemplVal('', '',
        #                      [LinkTypeData(OneTempLink('', []),
        #                                    OneTempLink('', []))
        #                       ]
        #                      )
        # print(swap.get_fields())
        # for one_templ in last_templ_swap.card.templates:
        #     for one_link in one_templ.many_temp_links:
        #         if one_link.val_links.the_link == swap.link_name and \
        #                 swap.pos - templ_pos in one_link.val_links.pos:
        #             _cur_link = one_link
        #             prev_str = self._res.res_str.last_successful
        #             # заменяем ссылку данного типа в конечной строке на её первичное значение
        #             # во всех указанных в текущем шаблоне позициях
        #             for one_pos in _cur_link.name_links.pos:
        #                 # print(self._res.res_str.last_successful)
        #                 # print(one_pos)
        #                 # print(templ_pos)
        #                 # print(self._res.res_str.last_successful[:one_pos+templ_pos])
        #                 # print(swap.link_val)
        #                 # print(swap.link_name)
        #                 # print(self._res.res_str.last_successful[one_pos + len(swap.link_name):])
        #                 rest_str = self._res.res_str.last_successful[one_pos + templ_pos +
        #                                                              len(swap.link_name):]
        #                 self._res.res_str.last_successful = (self._res.res_str.last_successful[:one_pos +
        #                                                                                         templ_pos] +
        #                                                      swap.link_val + rest_str
        #                                                      )
        #                 swapped_times += 1
        #                 # print(self._res.res_str.last_successful)
        #                 # print(last_templ_links_in_val_n)
        #                 # print(last_templ_links_in_name_n)
        #                 # print()
        #                 self._res.swaps += [
        #                     Swap(prev_str,
        #                          self._res.res_str.last_successful,
        #                          swap.link_val,
        #                          swap.link_name,
        #                          one_pos,
        #                          last_templ_swap.card)
        #                 ]
        #                 # if swapped_times == last_templ_links_in_name_n:
        #                 #    return None


def _all_links_vals_eq(self, used_links: List[LinkTypeData], last_templ_links_in_val_n: int):
    # for one_link in used_links:
    #     print(one_link.get_fields())
    # print(last_templ_links_in_val_n)
    # for i in range(last_templ_links_in_val_n):
    #     print(self._swaps[i-2].get_fields())
    return True