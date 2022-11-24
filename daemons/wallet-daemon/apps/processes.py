from .app import TronDaemon


class Core:

    daemon = (
        TronDaemon,
    )

    @classmethod
    def start(cls):
        pass
