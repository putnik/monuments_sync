# coding=utf-8

import pywikibot

PROPERTY_FUNCTIONS = {
    'P17': 'get_item',
    'P31': 'get_item',
    'P131': 'get_item',
    'P625': 'get_coordinate',
    'P1435': 'get_item',
    'P6375': 'get_address',
}


def get_label_data(title, page):
    return {
        'labels': {
            page.site.lang: {
                'language': page.site.lang,
                'value': title
            }
        }
    }


def get_address(value, repo):
    address = ', '.join(value)
    return pywikibot.WbMonolingualText(text=address, language='ru')


def get_coordinate(value, repo):
    precision = max(len(value[0].split('.')[1]), len(value[1].split('.')[1]))
    return pywikibot.Coordinate(lat=float(value[0]), lon=float(value[1]), precision=0.1 ** precision)


def get_item(value, repo):
    return pywikibot.ItemPage(repo, value)


def get_target(repo, pid, value):
    if pid not in PROPERTY_FUNCTIONS:
        return value

    function_name = PROPERTY_FUNCTIONS[pid]
    return globals()[function_name](value, repo)
