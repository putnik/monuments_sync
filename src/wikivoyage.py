# coding=utf-8

import pywikibot
from pywikibot import pagegenerators
from helpers import save_diff


def iterate_category(site, action, category_name=u'Категория:Списки культурного наследия России'):
    category = pywikibot.Category(site, category_name)
    generator = pagegenerators.CategorizedPageGenerator(category)
    for list_page in generator:
        action(list_page)


def update_list_page(list_page, old_text, new_text, page_update_summary=u'Update data'):
    if new_text != old_text:
        diff = save_diff(old_text, new_text)
        list_page.text = new_text
        list_page.save(page_update_summary)
        return diff
    return None
