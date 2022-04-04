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
def save_document(sid, message):
    print('save_document')
    print('save_document message : ',message , '********************************************************************\n')
    sio.emit('my_response_save_document', {'data': message}, room=sid)

@sio.event 
def get_document(sid, document_id):
    # wejsc do pooju
    # @sio.event
    # def join(sid, message):
    #     print('join')
    #     sio.enter_room(sid, message['room'])
    #     sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
    #             room=sid)

    print('join: ', document_id, '\n\n\n\n')
    sio.enter_room(sid, document_id)


    # wysąłnei do pokoju
    # @sio.event
    # def my_room_event(sid, message):
    #     print('my_room_event')
    #     sio.emit('my_response', {'data': message['data']}, room=message['room'])

    sio.emit('load_document', data=f'Dane pliku z serwera, {sid}, {document_id}', room=str(document_id))




# socket.broadcast.to(documentId).emit("receive-changes", delta);
@sio.event 
def receive_changes(sid, message):
    print('receive-changes')
    print('receive-changes message : ',message , '********************************************************************\n')
    sio.emit('my_response_receive-changes', {'data': message}, room=sid)


@sio.event
def send_changes(sid, data):
    print('*'*79)
    print('send_changes')
    print(data['documentId'])
    print(data['delta'])
    print('sid  ', sid)
    print('*'*79)
    print('\n\n\n\n')
    # sio.emit('send_changes.emit', {'data': message}, room=sid)
    # sid nie jest potrzebny to właściwie broadcast
    # sio.emit('send_changes.emit', {'data': message})
    
    # odłaczanie tego co wysyłał skip_sid

    sio.emit('receive-changes',data['delta'], room=data['documentId'], skip_sid=sid) #dla JS zdarzenie

