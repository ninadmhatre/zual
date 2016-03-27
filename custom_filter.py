__author__ = 'ninad'

import jinja2
import hashlib


def snippet(text, length=200):
    if text is None or not isinstance(text, str):
        return text

    t_snippet = text[:length]

    return t_snippet


def hash_me(text, prefix='some_text'):
    t = prefix + text
    md5 = hashlib.md5()
    md5.update(t.encode())
    return md5.hexdigest()

jinja2.filters.FILTERS['snippet'] = snippet
jinja2.filters.FILTERS['page_id'] = hash_me

# env = Environment()
# env.filters['snippet'] = snippet
