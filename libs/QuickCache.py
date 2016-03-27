# -*- coding: utf-8 -*-
author = 'ninad'

import pickle
from libs.RedisCache import RedisCache


class QuickCache(RedisCache):
    def __init__(self, host='localhost', port=6379):
        super().__init__(host, port)

    def pset(self, key, val, use_cache=True, **kwargs):
        if use_cache:
            self.set(key, pickle.dumps(val), **kwargs)

    def pget(self, key, use_cache=True):
        if use_cache:
            data = self.get(key)
            if data:
                return pickle.loads(data)
            return None
        else:
            return None
