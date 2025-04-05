from celery import Celery
import os

def make_celery():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return Celery('worker', broker=redis_url)

celery = make_celery()
