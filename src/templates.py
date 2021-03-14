# coding=utf-8

import re

PARAM_MAPPING = {
    'P17': 'region',
    'P18': 'image',
    'P31': 'type',
    'P131': 'munid',
    'P373': 'commonscat',
    'P625': ['lat', 'long'],
    'P1435': 'protection',
    'P1483': 'knid',
    'P5381': 'knid-new',
    'P6375': ['municipality', 'address'],
}

PROTECTION_VALUES = {
    u'Ф': 'Q23668083',
    u'Р': 'Q105835744',
    u'М': 'Q105835766',
    u'В': 'Q105835774',
}

TYPE_VALUES = {
    'archeology': 'Q839954',
    'architecture': 'Q2319498',
    'history': 'Q1081138',
    'monument': 'Q4989906',
    'settlement': 'Q3920245',
}


def get_protection_value(value):
    if value in PROTECTION_VALUES:
        return PROTECTION_VALUES[value]
    return None


def get_region_value(value):
    if not re.fullmatch("ru-[a-z]+", value):
        return None
    if value in ('ru-km', 'ru-sev'):
        # TODO: Add Ukraine
        pass
    return 'Q159'


def get_type_value(value):
    if value in TYPE_VALUES:
        return TYPE_VALUES[value]
    return None


def get_param_value(template, param):
    if type(param) in [list, tuple]:
        values = []
        for sub_param in param:
            value = get_param_value(template, sub_param)
            if value is None:
                return None
            values.append(value)
        return values

    if not template.has(param):
        return None
    value = template.get(param).value.strip()
    if value == "":
        return None

    if param == 'protection':
        return get_protection_value(value)
    if param == 'region':
        return get_region_value(value)
    if param == 'type':
        return get_type_value(value)

    return value


def check_template(template):
    return template.name.strip() == "monument"


def get_qid(template):
    qid = ''
    if template.has("wdid"):
        qid = template.get("wdid").value.strip()

    if re.fullmatch("Q\\d+", qid):
        return qid

    return None
