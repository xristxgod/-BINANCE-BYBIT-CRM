from typing import Type, Tuple

from apps.balancer.base import Balancer
import src.abstracts as abstracts


class CoreDaemon:

    def __init__(self, logger, node: Type[abstracts.AbstractNode]):
        self.logger = logger
        self.__node = node

    async def processing_block(self):
        pass

    async def processing_transaction(self):
        pass


class Daemon:
    cls_senders: Tuple[abstracts.AbstractSender] = ()

    api_client: Type[abstracts.AbstractAPIClient]
    balancer: Type[Balancer]
    node: Type[abstracts.AbstractNode]

    def __init__(self):
        pass

    async def thread(self):
        pass

    def run(self):
        while True:
            pass
