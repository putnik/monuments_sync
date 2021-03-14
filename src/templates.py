# coding=utf-8

import re

PARAM_MAPPING = {
    'P18': 'image',
    'P131': 'munid',
    'P373': 'commonscat',
    'P625': ['lat', 'long'],
    'P1483': 'knid',
    'P5381': 'knid-new',
}


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


def check_template(template):
    return template.name.strip() == "monument"


def get_qid(template):
    qid = ''
    if template.has("wdid"):
        qid = template.get("wdid").value.strip()

    if re.match("^Q\\d+$", qid):
        return qid

    return None
