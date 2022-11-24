import faker
from faker_crypto import CryptoAddress

import meta
import gateway.gate as gate
from gateway.schemas import BlockHeaderSchema, ParticipantSchema, TransactionSchema, BlockSchema, RawTransaction


class TestGateway(meta.Singleton, gate.BaseGateway):
    pass