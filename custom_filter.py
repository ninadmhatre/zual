__author__ = 'ninad'

import jinja2
import hashlib
from libs.Utils import Utility


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


def toBoolean(text):
    if isinstance(text, int):
        return text == 1
    return text.lower() in ('on', 'yes', 'true')


def toAscii(text):
    return Utility.unquote_string(text)


jinja2.filters.FILTERS['snippet'] = snippet
jinja2.filters.FILTERS['page_id'] = hash_me
jinja2.filters.FILTERS['toBoolean'] = toBoolean
jinja2.filters.FILTERS['toAscii'] = toAscii

# env = Environment()
# env.filters['snippet'] = snippet
