import os
import logging
from typing import Optional, Tuple, Dict

import settings


class MetaLogger(type):
    logger: Optional[logging.Logger]

    def __new__(mcs, class_name: str, bases: Tuple, attrs: Dict, **kwargs):
        obj = super(MetaLogger, mcs).__new__(mcs, class_name, bases, attrs)
        if attrs.get('path') is not None:
            logger = logging.getLogger('logger_' + class_name.lower())
            logger.setLevel(logging.INFO)
            if len(logger.handlers) < 1:
                handler = logging.FileHandler(os.path.join(settings.LOGS_DIR, attrs['path']), mode='a')
                formatter = logging.Formatter('%(asctime)s :: %(levelname)s\n%(message)s\n----------------')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            setattr(obj, 'logger', logger)
        return obj


class Logger(metaclass=MetaLogger):

    @classmethod
    def _send(cls, message: str):
        pass

    @classmethod
    def log(cls, message: str, *, method: str = 'info'):
        pass


def get_logger(logger_name: str):
    return type(
        logger_name.title(),
        (Logger,),
        {'path': f'{logger_name.lower()}.log'}
    )
