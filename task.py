#!/usr/bin/env python
# encoding: utf-8

#celery -A task worker --loglevel=info
#celery -A task beat  --loglevel=info

import time
import logging
from celery import Celery
from celery.schedules import timedelta

log = logging.getLogger('demo')


celery = Celery("demo", broker="amqp://admin:aidaijia.7788@192.168.10.232:5672/adj")
celery.conf.CELERY_RESULT_BACKEND = "amqp"

celery.conf.CELERYBEAT_SCHEDULE = {
    # 'add-every-10-seconds': {
    #      'task': 'task.schedule_test',
    #      'schedule': timedelta(seconds=10),
    # },
}

celery.conf.update(
    beat_schedule={
        'add-every-10-seconds': {
            'task': 'task.schedule_test',
            'schedule': timedelta(seconds=10),
        }
    }

)


@celery.task
def sleep(seconds):
    log.info("=================>" + str(seconds))
    time.sleep(float(seconds))
    return seconds


@celery.task
def schedule_test():
    log.info("==========================================>")

if __name__ == "__main__":
    celery.start()