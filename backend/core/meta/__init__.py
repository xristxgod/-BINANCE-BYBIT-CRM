import logging
import enum as e
from typing import NoReturn
from typing import Optional, Tuple, Dict


class Methods(e.Enum):
    DEBUG = 'debug'
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'
    CRITICAL = 'critical'


class MetaSingleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=MetaSingleton):
    pass


class MetaLogger(type):
    def __new__(mcs, class_name: str, bases: Tuple, attrs: Dict, **kwargs):
        logger_obj = super(MetaLogger, mcs).__new__(mcs, class_name, bases, attrs)
        if attrs.get('path') is not None:
            logger = logging.getLogger('logger_' + class_name.lower())
            logger.setLevel(logging.INFO)
            if len(logger.handlers) < 1:
                handler = logging.FileHandler(attrs['path'], mode='a')
                formatter = logging.Formatter('%(asctime)s :: %(levelname)s\n%(message)s\n----------------')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
            setattr(logger_obj, 'logger', logger)
        return logger_obj


class Logger(metaclass=MetaLogger):
    path: Optional[str] = None

    @classmethod
    def log(cls, message: str, method: Methods = Methods.INFO) -> NoReturn:
        getattr(cls.logger, method.value)(message)
