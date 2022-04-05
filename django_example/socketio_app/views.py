# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))

# 
# https://stackoverflow.com/questions/57579110/how-to-fix-access-control-allow-origin-error-in-a-python-socket-io-server
sio = socketio.Server(async_mode=async_mode, cors_allowed_origins='*')
# sio = socketio.Server(async_mode=async_mode)
thread = None


# baza danych
from .db_helper import get_or_create_note, update_note

def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    print('index')
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    print('background_thread')
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def my_event(sid, message):
    print('my_event')
    print('my_event message : ',message , '\n\n\n')
    sio.emit('my_response', {'data': message['data']}, room=sid)




@sio.event
def my_broadcast_event(sid, message):
    print('my_broadcast_event')
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    print('join')
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, room_name):
    # opuszczanie dokumentu
    print('leave')
    sio.leave_room(sid, room_name)
    sio.emit('my_response', {'data': 'Left room: ' + room_name},
             room=sid)


@sio.event
def close_room(sid, message):
    print('close_room')
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    print('my_room_event')
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    print('disconnect_request')
    sio.disconnect(sid)




@sio.event
def connect(sid, environ):
    print('Połączono z serwerem')
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')




###########################################################
@sio.event
def save_document(sid, data):
    print('---------------------save data---------------------')
    print('sid: ', sid)
    update_note(data['documentId'], data['data'])
    sio.emit('my_response_save_document', 'ala ma kota', room=data['documentId'] )

@sio.event 
def get_document(sid, document_id):
    # 1. wejsc do pooju o id dokumentu
    sio.enter_room(sid, document_id)
    # 2. pobrać dane dokuemntu {'_id':24ZnakowyHex, 'data':'String z danymi z edytora'}
    data = get_or_create_note(document_id)
    #3. wysłąć na front do zdarzenia 'load_document'
    sio.emit('load_document', data=data['data'], room=document_id)


@sio.event
def send_changes(sid, data):
    print('send_changes')
    print(data)
    
    update_note(data['documentId'], data['delta'])
    sio.emit('receive-changes',data['delta'], room=data['documentId'], skip_sid=sid) #dla JS zdarzenie

