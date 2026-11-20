from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import os

load_dotenv()

def make_celery(app_name='nyaysetu'):
    celery = Celery(app_name)
    redis_url = os.getenv('REDIS_URL', '')
    is_eager = True
    if redis_url and 'better-prawn-79965' not in redis_url:
        is_eager = False

    celery.conf.update(
        broker_url=redis_url if not is_eager else 'memory://',
        result_backend=redis_url if not is_eager else 'cache+memory://',
        task_always_eager=is_eager,
        broker_connection_retry_on_startup=True
    )
    
    # Configure Periodic Tasks (Automation)
    celery.conf.beat_schedule = {
        'annual-law-update': {
            'task': 'app.tasks.ai_tasks.sync_latest_laws_periodic',
            'schedule': crontab(0, 0, day_of_month='1', month_of_year='1'), # Jan 1st
        },
        'monthly-law-refresh': {
            'task': 'app.tasks.ai_tasks.sync_latest_laws_periodic',
            'schedule': crontab(0, 0, day_of_month='1'), # 1st of every month
        }
    }
    
    return celery

celery_app = make_celery()
