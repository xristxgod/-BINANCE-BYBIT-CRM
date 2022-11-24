import meta
import gateway.gate as gate


class TronGateway(meta.Singleton, gate.BaseGateway):
    cls_node = gate.tron.Node
