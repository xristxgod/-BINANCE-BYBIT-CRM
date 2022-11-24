import asyncio
from typing import Type, Optional, Dict, Tuple, List

import meta
import src.abstract as abstract
import gateway.gate as gate
from apps.balancer.base import Balancer
from src.schemas import TransactionSchema


# [{address: privateKey}, ...]
ADDRESSES = List[Dict[str: str]]


class CoreDaemon:

    def __init__(self, logger, gate_client: gate.GateClient, **config):
        self.logger = logger
        self.__gate_client = gate_client

        self.config = config

    async def processing_transaction(
            self, transaction: TransactionSchema, addresses: List[str]
    ) -> Optional[TransactionSchema]:
        get_addresses = lambda *lst: [p.address for p in lst]

        if self.config['only_inputs']:
            participants = get_addresses(*transaction.inputs)
        elif self.config['only_outputs']:
            participants = get_addresses(*transaction.outputs)
        else:
            participants = get_addresses(
                *transaction.outputs, *transaction.inputs
            )

        for participant in participants:
            if participant in addresses:
                return transaction
        return None

    async def accept(self, block_number: int, addresses: List[str]) -> List[TransactionSchema]:
        block = await self.__gate_client.block.get_block_by_id(block_number=block_number)
        if len(block.transactions) == 0:
            return []

        self.logger.log('{} :: Processing block: {}'.format(
            self.__class__.__name__, block_number
        ))
        transactions = await asyncio.gather(*[
            self.processing_transaction(
                transaction=transaction,
                addresses=addresses
            )
            for transaction in block.transactions
        ])
        self.logger.log('{} :: Transactions were found: {}'.format(
            self.__class__.__name__, any(transactions)
        ))
        return list(filter(lambda x: x is not None, transactions))


class Daemon:
    cls_senders: Tuple[abstract.AbstractSender] = ()

    client: Optional[Type[abstract.AbstractClient]] = None
    balancer: Optional[Type[Balancer]] = None
    gateway_client: Type[gate.BaseGateway]

    only_inputs = False
    only_outputs = False

    addresses: Optional[ADDRESSES] = None

    class DaemonError(Exception):
        pass

    class NotAddresses(DaemonError):
        pass

    class NotGoal(DaemonError):
        pass

    def __init__(self):
        self.validator()

        self.logger = meta.get_logger(self.__class__.__name__)

        self.gate_client = self.gateway_client.__call__(self.logger)
        self.client = self.client.__call__(self.logger)

        self.core = CoreDaemon(
            logger=self.logger,
            gate_client=self.gateway_client.gate,

            only_inputs=self.only_inputs,
            only_outputs=self.only_outputs
        )

    def validator(self):
        if self.addresses is None and self.client is None:
            raise self.NotAddresses()

        if len(self.cls_senders) == 0 and self.balancer is None:
            raise self.NotGoal()

        if self.only_inputs and self.only_outputs:
            self.only_inputs, self.only_outputs = False, False

    async def handler(self):
        self.logger.log('{} :: Start Interation'.format(
            self.__class__.__name__
        ))

        transactions = await self.core.accept()

    def run(self):
        while True:
            pass

    async def thread(self, **params):
        pass
