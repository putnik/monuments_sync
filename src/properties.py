# coding=utf-8

import pywikibot

TYPE_GLOBE_COORDINATE = 'globe-coordinate'
TYPE_ITEM = 'item'

PROPERTY_TYPES = {
    'P31': TYPE_ITEM,
    'P131': TYPE_ITEM,
    'P625': TYPE_GLOBE_COORDINATE,
    'P1435': TYPE_ITEM,
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


def get_coordinate(value):
    return pywikibot.Coordinate(lat=float(value[1]), lon=float(value[2]))


def get_target(repo, pid, value):
    if pid not in PROPERTY_TYPES:
        return value

    property_type = PROPERTY_TYPES[pid]
    if property_type == TYPE_GLOBE_COORDINATE:
        return get_coordinate(value)
    if property_type == TYPE_ITEM:
        return pywikibot.ItemPage(repo, value)

    return value
