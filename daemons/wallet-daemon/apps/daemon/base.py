from typing import Tuple


class AbstractSender:
    pass


class CoreDaemon:
    pass


class Daemon:
    cls_sender: Tuple[AbstractSender] = ()
    node: str

    def __init__(self):
        pass

    def run(self):
        pass
