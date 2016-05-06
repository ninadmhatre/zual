__author__ = 'ninad'

import logging
import logging.handlers
import enum


class LoggerTypes(enum.Enum):
    File = 0
    Mail = 1
    Console = 2


class AppLogger(object):
    def __init__(self, logger_config):
        self.logger_cfg = logger_config
        self.logger = None
        self.file_logger = None
        self.mail_logger = None
        self.console_logger = None

    def get_log_handler(self, logger_type=LoggerTypes.File):
        return self._configure_handler(logger_type)

    def get_stand_alone_logger(self):
        return self.logger

    def _configure_handler(self, logger_type):
        cfg = None

        if logger_type == LoggerTypes.File:
            logger = self.file_logger
            cfg = self.logger_cfg['FILE']
        elif logger_type == LoggerTypes.Mail:
            logger = self.mail_logger
            cfg = self.logger_cfg['MAIL']

        if self.logger is not None:
            return self.logger

        if cfg is None:
            return None

        # log = logging.getLogger('{0}_logger'.format(str(logger_type).lower()))
        self.logger = logging.getLogger(cfg['NAME'])

        handler = logging.handlers.TimedRotatingFileHandler(cfg['FILE'], **cfg['EXTRAS'])
        handler.setLevel(cfg['LEVEL'])
        handler.setFormatter(logging.Formatter(cfg['FORMAT']))

        self.logger.addHandler(handler)

        return handler
