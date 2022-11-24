import apps.balancer as balancer
import apps.daemon as daemon

import gateway
import src.services.client as client


class TronBalancer(balancer.Balancer):
    pass


class TronDaemon(daemon.Daemon):
    cls_senders = ()

    client = client.InternalClient
    balancer = TronBalancer
    gateway_client = gateway.TronGateway


__all__ = [
    'TronDaemon'
]
