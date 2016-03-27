# -*- coding: utf-8 -*-
__author__ = 'Ninad'

import os
import datetime


class Stats(object):
    def __init__(self, stat_dir):
        self.stats_dir = stat_dir
        self.download_stats = os.path.join(self.stats_dir, 'download.stats')
        self.view_stats = os.path.join(self.stats_dir, 'view.stats')

    def update_download_count(self, file_name, remote_addr):
        data = '{0}\t{1}\t{2}\n'.format(self._get_time(), remote_addr, os.path.basename(file_name))
        self._update(self.download_stats, data)

    def update_view_count(self, page, remote_addr):
        data = '{0}\t{1}\t{2}\n'.format(self._get_time(), remote_addr, page)
        self._update(self.view_stats, data)

    def get_download_count(self):
        data = self._read(self.download_stats).split('\n')
        return len(data)

    def get_download_stats(self):
        pass

    def get_view_count(self):
        pass

    def get_view_stats(self):
        pass

    def _get_time(self):
        return datetime.datetime.utcnow()

    def _update(self, x_file, data):
        with open(x_file, 'a') as f:
            f.write(data)
            f.flush()

    def _read(self, x_file):
        with open(x_file, 'r') as f:
            data = f.read()

        return data