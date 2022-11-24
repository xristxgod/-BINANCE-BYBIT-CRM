from .app import TronDaemon


class Core:

    daemon = (
        TronDaemon,
    )

    @classmethod
    def handler(cls):
        pass
