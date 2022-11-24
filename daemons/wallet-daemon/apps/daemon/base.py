from typing import Type, Tuple

import src.abstract as abstracts
import gateway.gate as gate
from apps.balancer.base import Balancer


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

    client: Type[abstracts.AbstractClient]
    balancer: Type[Balancer]
    gate_client: Type[gate.BaseGateway]

    def __init__(self):
        pass

    async def thread(self):
        pass

    def run(self):
        while True:
            pass
