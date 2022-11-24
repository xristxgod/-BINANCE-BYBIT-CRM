import decimal
from typing import Optional, Union

from tronpy.async_tron import AsyncContract, TAddress
from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

import src.settings as settings
import gateway.gate.base as base
from gateway.schemas import BlockHeaderSchema, ParticipantSchema, TransactionSchema, BlockSchema, RawTransaction


TOKENS = {
    'USDT': {'address': '...', 'decimals': 8}
}


class Node(base.AbstractNode):
    network_name = 'tron'
    endpoint_uri = settings.TRON_GATE_URL

    class SmartContract:
        @classmethod
        async def connect(cls, address: str) -> AsyncContract:
            return AsyncContract(address)

    def __init__(self):
        self.node = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.endpoint_uri))

        self.decimals = decimal.Context()
        self.decimals.prec = 8

    @staticmethod
    def from_sun(num) -> decimal.Decimal:
        if num == 0:
            return decimal.Decimal('0')
        if num < 0 or num > 2**256 - 1:
            raise ValueError("Value must be between 1 and 2**256 - 1")
        with decimal.localcontext() as ctx:
            ctx.prec = 999
            d_num = decimal.Decimal(value=num, context=ctx)
            result = d_num / decimal.Decimal("1000000")
        return result

    @staticmethod
    def to_sun(num) -> int:
        """
        Helper function that will convert a value in TRX to SUN
        :param num: Value in TRX to convert to SUN
        """
        if isinstance(num, int) or isinstance(num, str):
            d_num = decimal.Decimal(value=num)
        elif isinstance(num, float):
            d_num = decimal.Decimal(value=str(num))
        elif isinstance(num, decimal.Decimal):
            d_num = num
        else:
            raise TypeError("Unsupported type. Must be one of integer, float, or string")

        s_num = str(num)
        unit_value = decimal.Decimal("1000000")

        if d_num == 0:
            return 0

        if d_num < 1 and "." in s_num:
            with decimal.localcontext() as ctx:
                multiplier = len(s_num) - s_num.index(".") - 1
                ctx.prec = multiplier
                d_num = decimal.Decimal(value=num, context=ctx) * 10 ** multiplier
            unit_value /= 10 ** multiplier

        with decimal.localcontext() as ctx:
            ctx.prec = 999
            result = decimal.Decimal(value=d_num, context=ctx) * unit_value

        if result < 0 or result > 2**256 - 1:
            raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")

        return int(result)

    async def get_block(self, block_number: int) -> BlockSchema:
        response = await self.node.get_block(block_number)
        headers = BlockHeaderSchema(
            block=response['block_header']['raw_data']['number'],
            timestamp=response['block_header']['raw_data']['timestamp']
        )
        transactions = []
        for transaction in response['transactions']:
            token = None

            contract = transaction['raw_data']['contract']

            if contract[0]['type'] == 'TransferContract':
                amount = self.decimals.create_decimal(contract[0]['parameter']['value']['amount'])
                inputs = [ParticipantSchema(
                    address=contract[0]['parameter']['value']['owner_address'],
                    amount=amount
                )]
                outputs = [ParticipantSchema(
                    address=contract[0]['parameter']['value']['to_address'],
                    amount=amount
                )]
            elif contract['type'] == 'TriggerSmartContract' and 140 > len(contract[0]["parameter"]["value"]["data"]) > 130:
                data = contract[0]["parameter"]["value"]["data"]
                smart_contract = await self.SmartContract.connect(contract[0]["parameter"]["value"]["contract_address"])
                amount = int("0x" + data[72:], 0) / await smart_contract.functions.decimals
                inputs = [ParticipantSchema(
                    address=contract[0]['parameter']['value']['owner_address'],
                    amount=amount
                )]
                outputs = [ParticipantSchema(
                    address=self.node.to_base58check_address("41" + data[32:72]),
                    amount=amount
                )]
            else:
                continue

            transaction_fee = await self.node.get_transaction_info(transaction['txID'])
            if 'fee' not in transaction_fee:
                fee = self.from_sun(transaction_fee['fee'])
            else:
                fee = self.decimals.create_decimal('0')

            transactions.append(TransactionSchema(
                transactionId=transaction['txID'],
                amount=amount,
                fee=fee,
                inputs=inputs,
                outputs=outputs,
                timestamp=transaction['raw_data']['timestamp'],
                token=token
            ))

        return BlockSchema(
            headers=headers,
            transactions=transactions
        )

    async def get_latest_block_number(self) -> int:
        return await self.node.get_latest_block_number()

    async def get_balance(self, address: TAddress, token: Optional[str] = None) -> decimal.Decimal:
        if not token:
            amount = await self.node.get_account_balance(address)
        else:
            token = TOKENS[token]
            contract = await self.SmartContract.connect(token['address'])
            amount = await contract.functions.balanceOf(address)
            if amount > 0:
                amount = amount / 10 ** token['decimals']

        return self.decimals.create_decimal(amount)

    async def create_transaction(
            self, from_: TAddress, to: TAddress, amount: decimal.Decimal, token: Optional[str] = None
    ) -> RawTransaction:
        if not token:
            raw_data = self.node.trx.transfer(from_, to=to, amount=self.to_sun(amount))
        else:
            pass

        raise NotImplementedError

    async def sing_transaction(self, raw_data: str, private_key: str) -> str:
        raise NotImplementedError

    async def send_transaction(self, raw_transaction: str) -> TransactionSchema:
        raise NotImplementedError


class GateClient(base.BaseGateClient):
    cls_node = Node
