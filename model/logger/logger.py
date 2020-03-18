import logging
import time
import pathlib
import os


class Logger:

    active_loggers = {}
    level = logging.CRITICAL
    logger_dir = '.'

    def __init__(self, logger_name, filename, prefix=None):
        self.prefix = prefix + ' ' if prefix is not None else ''
        self.logger = self.set_up_logger(logger_name, filename)

    def debug(self, msg):
        self.logger.debug(self.prefix + msg)

    def info(self, msg):
        self.logger.info(self.prefix + msg)

    def warning(self, msg):
        self.logger.warning(self.prefix + msg)

    @staticmethod
    def get_dir():
        return str(Logger.logger_dir)

    def set_up_logger(self, logger_name, filename, prefix=None):
        if logger_name in self.active_loggers:
            return self.active_loggers[logger_name]
        else:
            # Set up a specific logger with our desired output level
            logger = logging.getLogger(logger_name)
            # logger.setLevel(logging.DEBUG)
            logger.setLevel(Logger.level)
            timestr = time.strftime("%Y-%m-%d-%H:%M")
            p = pathlib.PurePath(filename)
            parent = p.parent
            name = p.name
            path = parent.joinpath(timestr).joinpath(name)
            os.makedirs(path.parent, exist_ok=True)
            Logger.logger_dir = path.parent
            handler = logging.FileHandler(str(path), mode='a')
            # handler.setLevel(logging.DEBUG)
            handler.setLevel(Logger.level)
            # create formatter
            if prefix:
                formatter = logging.Formatter("[%(levelname)s] {} %(asctime)s - %(message)s".format(prefix))
            else:
                formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
            # add formatter to ch
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            self.active_loggers[logger_name] = logger
            return logger
