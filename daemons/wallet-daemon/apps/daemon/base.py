from typing import Tuple

from src.abstracts import AbstractSender


class CoreDaemon:
    pass


class Daemon:
    cls_senders: Tuple[AbstractSender] = ()
    node: str

    def __init__(self):
        pass

    def run(self):
        pass
