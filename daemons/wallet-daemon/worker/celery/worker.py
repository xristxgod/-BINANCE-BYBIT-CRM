import asyncio
from typing import Coroutine

from apps.balancer import Balancer, BalancerThread

from worker.celery.app import app


def run_async(func: Coroutine):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)


@app.task(acks_late=True)
def start_balancer(balancer: Balancer):
    run_async(balancer.handler())


@app.task(acks_late=True)
def start_balancer_thread(balancer_thread: BalancerThread):
    run_async(balancer_thread.handler())
