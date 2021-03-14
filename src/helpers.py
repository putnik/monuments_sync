# coding=utf-8

from difflib import ndiff
from hashlib import md5


def debug(data):
    print(data.encode('utf8'))


def log(string):
    print(string)
    with open('data/log', 'a') as file:
        file.write('%s\n' % string.encode('utf8'))


def publish_log():
    pass


def save_to_file(path, text):
    text = str(text)
    md5_hash = md5(text.encode('utf8'))
    with open('data/%s/%s' % (path, md5_hash), 'w') as file:
        file.write(text)
    return md5_hash


def save_cache(text):
    return save_to_file('cache', text)


def save_diff(old_text, new_text):
    diff = ndiff(old_text.encode('utf8'), new_text.encode('utf8'))
    return save_to_file('diff', diff)
