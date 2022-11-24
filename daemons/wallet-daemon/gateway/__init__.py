import meta
import gateway.gate as gate


class TronGateway(meta.Singleton):
    gate_client = gate.tron.Node
