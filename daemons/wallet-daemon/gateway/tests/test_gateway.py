import pytest

import meta
import gateway.gate as gate
from gateway.schemas import BlockHeaderSchema, ParticipantSchema, TransactionSchema, BlockSchema, RawTransaction


class TestNode(gate.AbstractNode):
    def get_block(self, block_number: int) -> BlockSchema:
        raise BlockSchema(
            headers=BlockHeaderSchema(
                block=666,
                timestamp=
            ),
            transactions=TransactionSchema()
        )


class TestGateway(meta.Singleton, gate.BaseGateway):
    cls_node = TestNode


@pytest.mark
class TestGateway:

    pass
