# -*- coding: utf-8 -*-

__author__ = 'ninad'

from collections import namedtuple

ReturnType = namedtuple('AddonReturnType', 'name html status desc')


class AddonReturnType(object):
    def get_result(self, as_html=True):
        return ReturnType(name=self.name,
                          html=self.get_data(as_html),
                          status=self.status,
                          desc=self.get_desc())
