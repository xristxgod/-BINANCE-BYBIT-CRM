from typing import Type, Tuple

from apps.balancer.base import Balancer
from src.abstracts import AbstractSender, AbstractNode


class CoreDaemon:

    def __init__(self, logger, node: Type[AbstractNode]):
        pass

    async def processing_block(self):
        pass

    async def processing_transaction(self):
        pass


class Daemon:
    cls_senders: Tuple[AbstractSender] = ()
    balancer: Type[Balancer]
    node: Type[AbstractNode]

    def __init__(self):
        pass

    async def thread(self):
        pass

    def run(self):
        while True:
            pass
