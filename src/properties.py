# coding=utf-8

import pywikibot

PROPERTY_FUNCTIONS = {
    'P17': 'get_item',
    'P31': 'get_item',
    'P131': 'get_item',
    'P625': 'get_coordinate',
    'P1435': 'get_item',
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


def get_address(value):
    return ', '.join(value)


def get_coordinate(value):
    return pywikibot.Coordinate(lat=float(value[1]), lon=float(value[2]))


def get_target(repo, pid, value):
    if pid not in PROPERTY_FUNCTIONS:
        return value

    function_name = PROPERTY_FUNCTIONS[pid]
    return locals()[function_name](value)
