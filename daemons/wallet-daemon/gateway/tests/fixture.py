import random

import faker
from faker_crypto import CryptoAddress

import pytest

from src.schemas import BlockHeaderSchema, ParticipantSchema, TransactionSchema, BlockSchema

fake = faker.Faker()
fake.add_provider(CryptoAddress)


@pytest.fixture()
def transaction(timestamp: int = None):
    amount = fake.unique.pydecimal(right_digits=8, min_value=10, max_value=1_000)

    if timestamp is None:
        timestamp = fake.unique.unix_time()

    return TransactionSchema(
        transactionId=fake.unique.sha256(),
        amount=amount,
        fee=fake.unique.pydecimal(right_digits=8, min_value=0, max_value=10),
        inputs=[ParticipantSchema(
            address=fake.unique.ethereum_address(),
            amount=amount
        )],
        outputs=[ParticipantSchema(
            address=fake.unique.ethereum_address(),
            amount=amount
        )],
        timestamp=timestamp,
        token=random.choices(['USDT', None])[0]
    )


@pytest.fixture()
def block_headers(timestamp: int):
    if timestamp is None:
        timestamp = fake.unique.unix_time()
    return BlockHeaderSchema(
        block=fake.unique.random_int(min=1_000, max=999_999),
        timestamp=timestamp
    )


@pytest.fixture()
def block(block_headers, transaction):
    timestamp = fake.unique.unix_time()
    return BlockSchema(
        headers=block_headers(timestamp=timestamp),
        transactions=[
            transaction(timestamp=timestamp)
            for tx in range(random.randrange(1, 10))
        ]
    )
