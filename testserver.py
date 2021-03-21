from flask import Flask
from flask_socketio import SocketIO, disconnect, emit, send, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


@sio.on('connect')
def connect_handler():
    emit('connection_response',
             {'message': 'Test joined'},
             broadcast=True)

@sio.on('get_user_data')
def get_user_data():
    try:
        resTESTObject = {
            'user': {"uid":"6053555ad795fcfee85dbdc5","email":"1@1.de","username":"1","password_hash":"d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35","created_poject_pids":["6055c6a0b58a129e10222bf9"],"collab_poject_pids":[],"default_editor":True}
        }

        emit('user_response', {
            'message': 'Successfull',
            'value': resTESTObject
        },
            broadcast=False)
    except Exception as e:
        emit('user_response', {
            "message": "Error"
        },
            broadcast=False)

@sio.on('join')
def join_document():
    join = {'message': '1@1 has joined 6055c6a0b58a129e10222bf8'}
    emit('join_response', join)

@sio.on('leave')
def leave_document():
    leave = {'message': '1@1 has left 6055c6a0b58a129e10222bf8'}
    emit('leave_response', leave)

@sio.on('open_document')
def open_document():
    open_document_Object = {
            'message': 'Successfull',
            'value': {
                'text': {"0000-1616234144": [["0001-1616266858730", "a"],
                    ["0002-1616266854779", "s"],
                    ["0002-1616266858878", "b"],
                    ["0003-1616266859069", "c"],
                    ["0004-1616266859326", "d"],
                    ["0005-1616266859482", "e"],
                    ["0006-1616266859728", "f"]
                    ] 
                }
            }
        }
    emit('open_document_response', open_document_Object )

@sio.on('get_project')
def get_project_data(pid):
    projektTest = {"message": "Successful",
            "value": {"main":{"_id":"6055c6a0b58a129e10222bf7","name":"main","dids":["6055c6a0b58a129e10222bf8"],"folders":[],"images":[]}}
    }
    emit('get_project_response', projektTest)

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)


