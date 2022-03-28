"# django_python-socketio_simple" 

# django app example
https://github.com/miguelgrinberg/python-socketio/tree/main/examples/server/wsgi/django_example



### The WebSocket transport is not available, you must install a WebSocket server that is compatible with your async mode to enable it. See the documentation for details.
https://stackoverflow.com/questions/69082602/the-websocket-transport-is-not-available-you-must-install-a-websocket-server-th
// pip install gevent-websocket # works without it
pip install eventlet

### wsgi plik
https://stackoverflow.com/questions/48925318/raise-runtimeerroryou-need-to-use-the-eventlet-server

```

virtualenv env
env\Scripts\activate.bat

pip install Django
pip install python-socketio
pip install eventlet

django-admin startproject django_example
cd django_example
python manage.py startapp socketio_app


```
