# -*- coding: utf-8 -*-
author = 'ninad'

import redis


class RedisCache(object):
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.conn = self._connect()
        self.offline = self._check_availibility()

    def _connect(self):
        return redis.Redis(host=self.host, port=self.port, encoding='utf-8')

    def _check_availibility(self):
        try:
            result = self.conn.ping()
        except redis.exceptions.ConnectionError:
            return True
        else:
            return False

    def set(self, key, val, timeout=86400, **kwargs):
        """
        Set key with timeout default with 12 hrs
        :param string key:
        :param bool permanent:
        :param object val:
        :param int timeout:
        :return:
        """
        if not self.offline:
            self.conn.setex(key, val, timeout)

    def rm(self, key):
        if not self.offline:
            self.conn.delete(key)

    def get(self, key):
        if not self.offline:
            return self.conn.get(key)
        return None

    def info(self):
        if not self.offline:
            return self.conn.info(section='all')
        return None