# coding=utf-8

import pywikibot

TYPE_COMMONS_MEDIA = 'commonsMedia'
TYPE_EXTERNAL_ID = 'external-id'
TYPE_GLOBE_COORDINATE = 'globe-coordinate'
TYPE_ITEM = 'item'
TYPE_STRING = 'string'

PROPERTY_TYPES = {
    'P18': TYPE_COMMONS_MEDIA,
    'P131': TYPE_ITEM,
    'P373': TYPE_STRING,
    'P625': TYPE_GLOBE_COORDINATE,
    'P1483': TYPE_EXTERNAL_ID,
    'P5381': TYPE_EXTERNAL_ID,
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
    property_type = PROPERTY_TYPES[pid]
    if property_type == TYPE_GLOBE_COORDINATE:
        return get_coordinate(value)
    if property_type == TYPE_ITEM:
        return pywikibot.ItemPage(repo, value)

    return value
