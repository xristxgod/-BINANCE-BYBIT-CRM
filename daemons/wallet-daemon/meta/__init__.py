import os
import logging
from typing import Optional, Tuple, Dict

import src.settings as settings


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaLogger(type):
    logger: Optional[logging.Logger]

    def __new__(mcs, class_name: str, bases: Tuple, attrs: Dict, **kwargs):
        logger_obj = super(MetaLogger, mcs).__new__(mcs, class_name, bases, attrs)
        if attrs.get('path') is not None:
            logger = logging.getLogger('logger_' + class_name.lower())
            logger.setLevel(logging.INFO)
            if len(logger.handlers) < 1:
                handler = logging.FileHandler(os.path.join(settings.LOGS_DIR, attrs['path']), mode='a')
                formatter = logging.Formatter('%(asctime)s :: %(levelname)s\n%(message)s\n----------------')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            setattr(logger_obj, 'logger', logger)
        return


class Logger(metaclass=MetaLogger):
    pass


class Singleton(metaclass=SingletonMeta):
    pass
