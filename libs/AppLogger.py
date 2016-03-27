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
        self.file_logger = None
        self.mail_logger = None
        self.console_logger = None

    def get_log_handler(self, logger_type=LoggerTypes.File):
        return self._configure_handler(logger_type)

    def _configure_handler(self, logger_type):
        log = None
        cfg = None
        if logger_type == LoggerTypes.File:
            log = self.file_logger
            cfg = self.logger_cfg['FILE']
        elif logger_type == LoggerTypes.Mail:
            log = self.mail_logger
            cfg = self.logger_cfg['MAIL']

        if log is not None:
            return log

        if cfg is None:
            return None

        logger = logging.getLogger(cfg['NAME'])

        handler = logging.handlers.TimedRotatingFileHandler(cfg['FILE'], **cfg['EXTRAS'])
        handler.setLevel(cfg['LEVEL'])
        handler.setFormatter(logging.Formatter(cfg['FORMAT']))

        logger.addHandler(handler)
        return handler
