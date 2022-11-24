import pytest

import meta
import gateway.gate as gate


class TestNode(gate.AbstractNode):
    pass


class TestGateway(meta.Singleton, gate.BaseGateway):
    cls_node = TestNode


@pytest.mark
class TestGateway:

    pass
