from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django setting module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'javagochi_server.settings')
app = Celery('javagochi_server', include = ['javagochi.tasks'])

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
