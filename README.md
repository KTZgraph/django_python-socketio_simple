"# django_python-socketio_simple" 

-------------------------------------- DJANGO --------------------------------------

# django app example
https://github.com/miguelgrinberg/python-socketio/tree/main/examples/server/wsgi/django_example



### The WebSocket transport is not available, you must install a WebSocket server that is compatible with your async mode to enable it. See the documentation for details.
https://stackoverflow.com/questions/69082602/the-websocket-transport-is-not-available-you-must-install-a-websocket-server-th
// pip install gevent-websocket # works without it
pip install eventlet

### wsgi file django_example\django_example\wsgi.py
https://stackoverflow.com/questions/48925318/raise-runtimeerroryou-need-to-use-the-eventlet-server

### create
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


### run
```
cd django_example 
python manage.py runserver
```

-------------------------------------- REACT --------------------------------------

https://www.youtube.com/watch?v=iRaelG7v0OU



------------------------- CORS
### Access to XMLHttpRequest at 'http://127.0.0.1:8000/socket.io/?EIO=4&transport=polling&t=N_IYx0M' from origin 'http://127.0.0.1:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.

https://stackoverflow.com/questions/57579110/how-to-fix-access-control-allow-origin-error-in-a-python-socket-io-server

// change this in wsgi.file

sio = socketio.Server()
Use

sio = socketio.Server(cors_allowed_origins='*')


https://github.com/miguelgrinberg/python-socketio/blob/main/docs/server.rst