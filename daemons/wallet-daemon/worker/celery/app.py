from celery import Celery

import settings


app = Celery(
    "worker",
    backend=Config.REDIS_URL,
    broker=Config.RABBITMQ_URL
)
app.conf.task_routes = {
    "worker.celery_worker.send_transaction": "test-queue",

}

app.conf.update(task_track_started=True)
