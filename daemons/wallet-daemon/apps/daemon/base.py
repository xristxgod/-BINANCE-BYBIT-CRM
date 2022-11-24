from typing import Type, Tuple

import src.abstract as abstract
import gateway.gate as gate
from apps.balancer.base import Balancer

import meta


class CoreDaemon:

    def __init__(self, logger, gate_client: gate.GateClient):
        self.logger = logger
        self.__gate_client = gate_client

    async def processing_blocks(self):
        pass

    async def processing_transaction(self):
        pass


class Daemon:
    cls_senders: Tuple[abstract.AbstractSender] = ()

    client: Type[abstract.AbstractClient]
    balancer: Type[Balancer]
    gateway_client: Type[gate.BaseGateway]

    def __init__(self):
        self.logger = meta.get_logger(self.__class__.__name__)

        self.gate_client = self.gateway_client.__call__(self.logger)
        self.client = self.client.__call__(self.logger)

        self.core = CoreDaemon(
            logger=self.logger,
            gate_client=self.gateway_client.gate
        )

    async def thread(self):
        pass

    def run(self):
        while True:
            pass
