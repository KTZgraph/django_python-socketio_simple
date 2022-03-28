"""
WSGI config for django_example project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_example.settings')

# application = get_wsgi_application()


# https://stackoverflow.com/questions/48925318/raise-runtimeerroryou-need-to-use-the-eventlet-server
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.settings")

from socketio import Middleware
from socketio_app.views import sio
django_app = get_wsgi_application()
application = Middleware(sio, django_app)

#
import eventlet
import eventlet.wsgi
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)