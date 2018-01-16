# coding; utf-8
import logging

from config.logConfig import *


def __set_level(config):
    if config == 'DEBUG':
        return logging.DEBUG
    elif config == 'INFO':
        return logging.INFO
    elif config == 'WARNING':
        return logging.WARNING
    elif config == 'ERROR':
        return logging.ERROR


# console
_console = logging.StreamHandler()
_console.setLevel(__set_level(LOG["console"]["level"]))
_formatter = logging.Formatter(fmt=LOG["console"]["fommat"], datefmt=LOG["console"]["datefmt"])
_console.setFormatter(_formatter)

# file
_filehandler = logging.FileHandler(filename=LOG["file"]["path"], encoding="utf-8")
_filehandler.setLevel(__set_level(LOG["file"]["level"]))
_fmter = logging.Formatter(fmt=LOG["file"]["fommat"], datefmt=LOG["file"]["datefmt"])
_filehandler.setFormatter(_fmter)


class BaseLog(object):
    def __init__(self, name: str):
        logging.basicConfig(level=logging.DEBUG, handlers=[_console, _filehandler])
        self.log = logging.getLogger(name)


if __name__ == '__main__':
    log = BaseLog("Test").log
    log.debug("this is debug msg")
    log.info("this is info msg")
    log.warning("this is warning msg")
    log.error("this is error msg")

    log.info("this is a format: %s %s", "hello", "world")

    log.info("this is info msg 爱爱爱")
    try:
        raise Exception("aaa")
    except Exception  as e:
        log.exception("Exception happened")

    print("end")
