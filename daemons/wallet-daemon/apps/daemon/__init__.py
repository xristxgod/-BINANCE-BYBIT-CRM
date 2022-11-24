import time
import asyncio
import dataclasses
from typing import NoReturn, Type, Optional, Dict, Tuple, List

import meta
import src.abstract as abstract
import gateway.gate as gate
from apps.balancer import Balancer
from src.schemas import MessageSchemas, MessageHeadersSchemas, TransactionSchema

from worker.celery import celery_storage, celery_app


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

    async def processing_block(self, block_number: int, addresses: List[str]) -> List[TransactionSchema]:
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

    async def handler(self, addresses: List[str]) -> Optional[MessageSchemas]:
        try:
            block_number = await self.__gate_client.block.get_block_in_storage()
            if block_number >= await self.__gate_client.block.get_latest_block_number():
                await asyncio.sleep(10)
                return None
            transactions = await self.processing_block(block_number, addresses=addresses)
        except Exception as error:
            # Обработать случай когда что то сломалось и транзакция не обратоталсь
            raise
        else:
            await self.__gate_client.block.save_block_to_storage(block_number + 1)

        return MessageSchemas(
            headers=MessageHeadersSchemas(
                blockNumber=block_number,
                timestamp=int(time.time()),
                network=self.__gate_client.node.network
            ),
            body=transactions
        )


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

        self.gateway_client: gate.BaseGateway = self.gateway_client.__call__(self.logger)

        if self.client is not None:
            self.client: abstract.AbstractClient = self.client.__call__(self.logger)

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

    async def handler_sender(self, message: MessageSchemas) -> NoReturn:
        for cls_sender in self.cls_senders:
            message = dataclasses.asdict(message)
            self.logger.log('{} :: Sender manager: {} :: Send message: {}'.format(
                self.__class__.__name__, cls_sender.__class__.__name__, message
            ))
            await cls_sender.send(message=message)

    async def handler_balancer(self, message: MessageSchemas) -> NoReturn:
        self.logger.log('{} :: Send to Balancer :: Message: {}'.format(
            self.__class__.__name__, dataclasses.asdict(message)
        ))

        balancer = self.balancer(
            message=message,
            gateway_client=self.gateway_client,
            client=self.client,
            addresses=self.addresses,
            logger=self.logger
        )
        try:
            can_go, wait_time = await celery_storage.can_go(
                'start_balancer_balancer_{}'.format(message.headers.blockNumber)
            )
            extra = {"countdown": wait_time} if not can_go and wait_time > 5 else {}
            celery_app.send_task(
                f'worker.celery.worker.start_balancer',
                args=[balancer],
                **extra
            )
        except Exception as error:
            self.logger.log('{} :: Send to Balancer :: Failed'.format(
                self.__class__.__name__
            ))
            raise
        else:
            self.logger.log('{} :: Send to Balancer :: Success'.format(
                self.__class__.__name__
            ))

    async def handler(self):
        addresses = self.addresses if self.addresses is not None else await self.client.get_wallets()

        self.logger.log('{} :: Start Interation :: Addresses: {}'.format(
            self.__class__.__name__, addresses
        ))

        message = await self.core.handler(addresses=addresses)

        if message is not None:
            if len(self.cls_senders) != 0:
                await self.handler_sender(message)

            if self.balancer is not None:
                await self.handler_balancer(message)

        self.logger.log('{} :: End iteration :: Addresses: {}'.format(
            self.__class__.__name__, addresses
        ))

    def run(self):
        while True:
            await self.handler()
            await asyncio.sleep(1)

    async def thread(self, **params):
        raise NotImplementedError
