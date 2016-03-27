
__author__ = 'Ninad Mhatre'

from addonpy.IAddonInfo import IAddonInfo


class SiteStatsAddon(IAddonInfo):
    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def execute(self):
        raise NotImplemented

    @staticmethod
    def __addon__():
        return 'SiteStatsAddon'
