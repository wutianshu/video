# coding: utf-8
import datetime, time
from celery import task

@task
def sayHello():
    print(datetime.datetime.now())
    time.sleep(5)
    print(datetime.datetime.now())
