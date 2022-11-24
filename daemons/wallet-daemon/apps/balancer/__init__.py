from typing import Optional

import meta
from src.schemas import MessageSchemas, BalancerThreadMessage
from gateway.gate import BaseGateway
from src.abstract import AbstractClient


class BalancerThread:
    def __init__(
            self, message: BalancerThreadMessage,
            gateway_client: BaseGateway,
            client: Optional[AbstractClient] = None,
            logger=None
    ):
        self.message = message
        self.gateway_client = gateway_client

        if client is not None:
            self.client = client

        if logger is None:
            logger = meta.get_logger(self.__class__.__name__)
        self.logger = logger

    async def handler(self):
        pass


class Balancer:

    client: Optional[AbstractClient] = None

    def __init__(
            self, message: MessageSchemas,
            gateway_client: BaseGateway,
            client: Optional[AbstractClient] = None,
            logger=None
    ):
        self.message = message
        self.gateway_client = gateway_client

        if client is not None:
            self.client = client

        if logger is None:
            logger = meta.get_logger(self.__class__.__name__)
        self.logger = logger

    async def handler(self):
        pass

