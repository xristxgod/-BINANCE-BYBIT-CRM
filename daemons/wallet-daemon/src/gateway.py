import logging
from typing import Optional, Dict
from datetime import datetime, timedelta

from aiohttp import ClientSession
from async_property import async_property, async_cached_property

import meta
import src.settings as settings
import src.schemas as schemas


class GateClient(meta.Singleton):

    url = settings.INTERNAL_URI

    login = settings.INTERNAL_LOGIN
    password = settings.INTERNAL_PASSWORD

    session_client = ClientSession

    __slots__ = (
        'token', 'token_expires', 'logger', 'session'
    )

    class ClientException(Exception):
        pass

    class AuthRequired(ClientException):
        pass

    def __init__(self, logger: logging):
        self.token: Optional[datetime] = None
        self.token_expires: Optional[datetime] = None

        self.logger = logger

    async def _refresh_token(self):
        pass

    @async_property
    async def headers(self) -> Dict:
        if not self.token or self.token_expires < datetime.now() - timedelta(hours=1):
            await self._refresh_token()
        return {'Content-Type': 'application/json', 'X-TOKEN-AUTH': self.token}

    async def session(self, headers: Dict = None) -> ClientSession:
        async with self.session_client(headers=headers) as session:
            yield session

    async def request(self, method: str, path: str, data: Dict, headers: Dict = headers):
        async with self.session(headers=headers).request(method, url=self.url+path, data=data) as response:
            return await response.json()


class InternalGateway(meta.Singleton):
    gate_client = GateClient

    def __init__(self, logger: logging):
        self.client = self.gate_client(logger)

    def get_all_wallet(self, network: schemas.Network = schemas.Network.tron) -> schemas.Wallet:
        pass
