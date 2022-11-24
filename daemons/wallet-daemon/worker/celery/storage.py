from typing import Dict
from datetime import datetime, timedelta

import meta


class Storage(meta.Singleton):

    def __init__(self):
        import asyncio

        self.lock = asyncio.Lock()
        self.tasks: Dict[str: datetime] = {}

    async def accept(self, name: str):
        async with self.lock:
            if name not in self.tasks:
                self.tasks.update({name: datetime.now()})

            seconds = (datetime.now() - self.tasks[name]).seconds
            if seconds > 60:
                self.tasks.update({name: datetime.now()})
                return True, 0
            else:
                self.tasks.update({name: self.tasks[name] + timedelta(seconds=60-seconds)})
                return False, 60 - seconds


storage = Storage()
