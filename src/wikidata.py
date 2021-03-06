# coding=utf-8

import pywikibot

item_create_summary = u'Import data from [[voy:ru:%s]]'
item_update_summary = u'Import updated data from [[voy:ru:%s]]'


def get_label_data(title, page):
    return {
        'labels': {
            page.site.lang: {
                'language': page.site.lang,
                'value': title
            }
        }
    }


def get_label(item, list_page):
    item_dict = item.get()
    if 'labels' not in item_dict or list_page.site.lang not in item_dict['labels']:
        return None
    if item_dict['labels'][list_page.site.lang] == '':
        return None

    return item_dict['labels'][list_page.site.lang]


def update_label(item, title, list_page):
    label_data = get_label_data(title, list_page)
    item.editEntity(label_data, summary=item_update_summary % list_page.title())


def get_new_item(repo, list_page, title):
    item = pywikibot.ItemPage(repo)
    data = get_label_data(title, list_page)
    item.editEntity(data, summary=item_create_summary % list_page.title())
    return item


def add_source(repo, list_page, claim, template):
    ruwv_claim = pywikibot.Claim(repo, 'P143')
    ruwv_target = pywikibot.ItemPage(repo, 'Q17601812')
    ruwv_claim.setTarget(ruwv_target)

    page_claim = pywikibot.Claim(repo, 'P4656')
    page_target = 'https://ru.wikivoyage.org/?oldid=%s' % list_page.latest_revision_id
    if template.has('knid'):
        page_target += '#' + template.get('knid').value.strip()
    page_claim.setTarget(page_target)

    claim.addSources([ruwv_claim, page_claim])


def add_claim(repo, list_page, item, pid, target, template):
    item_dict = item.get()

    if "claims" in item_dict and pid in item_dict["claims"]:
        return  # TODO: Find item with correct source if possible

    claim = pywikibot.Claim(repo, pid)
    claim.setTarget(target)
    item.addClaim(claim)
    add_source(repo, list_page, claim)
