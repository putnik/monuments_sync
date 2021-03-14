# coding=utf-8

import mwparserfromhell
import pywikibot

from helpers import log, publish_log, save_cache, debug
from properties import get_target
from templates import get_param_value, check_template, get_qid
from wikidata import add_claim, get_new_item, update_label
from wikivoyage import update_list_page, iterate_category

site = pywikibot.Site('ru', 'wikivoyage')
repo = site.data_repository()

PARAM_MAPPING = {
    'P18': 'image',
    'P131': 'munid',
    'P373': 'commonscat',
    'P625': ['lat', 'long'],
    'P1483': 'knid',
    'P8316': 'sobory',
    'P5381': 'knid-new',
}


def update_item_claims(item, template, list_page):
    for pid in PARAM_MAPPING:
        param = PARAM_MAPPING[pid]
        value = get_param_value(template, param)
        if value is None:
            continue

        log(u'** %s = "%s"' % (pid, value))
        target = get_target(repo, pid, value)
        add_claim(repo, list_page, item, pid, target)
        # exit()  # FIXME


def create_item(template, list_page):
    if not template.has('name'):
        log(u'** !!empty name!!')
        return

    label = template.get('name').value.strip()
    item = get_new_item(repo, list_page, label)
    qid = 'Q%s' % item.getID()
    log(u'* (new) [[d:Q%s]] = "%s"' % (qid, label))

    # TODO: description

    template.replace('wdid', qid)
    cache_hash = save_cache(list_page)
    log(u'** update list: wdid=%s (cache: %s)' % (qid, cache_hash))

    return template


def update_item(template, list_page):
    qid = template.get('wdid').value.strip()
    log(u'* [[d:%s]]' % qid)

    item = pywikibot.ItemPage(repo, qid)
    if not item.exists():
        log(u'** !!WRONG wdid!!')
        return

    if item.getLabel() == '':
        update_label(item, template.title, list_page)
        log(u'** new label: "%s"' % template.title)

    update_item_claims(item, template, list_page)

    return template


def process_list_page(list_page):
    log(u'== [[%s]] ==' % list_page.title())

    text = list_page.get()
    code = mwparserfromhell.parse(text)
    for template in code.filter_templates():
        if not check_template(template):
            continue
        debug(template)
        qid = get_qid(template)
        if qid is None:
            create_item(template, list_page)
            break  # FIXME
        else:
            update_item(template, list_page)

    diff = update_list_page(list_page, text, code)
    if diff is None:
        log(u': skipped')
    else:
        log(u': updated (diff: %s)' % diff)


iterate_category(site, process_list_page)
# process_list_page(pywikibot.Page(site, 'Культурное наследие России/Вологодская область/Вологда'))
publish_log()
