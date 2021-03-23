from flask import Flask, request, jsonify
from flask_socketio import SocketIO, disconnect, emit, send, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

mock_user_data = [
    {
        "uid": "6053555ad795fcfee85dbdc5",
        "email": "1@1.de",
        "username": "1",
        "password_hash": "d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab36",
        "created_poject_pids": [
            "6055c6a0b58a129e10222bf7"
        ],
        "collab_poject_pids": [],
        "default_editor": True
    },
    {
        "uid": "6053555ad795fcfee85dbdc6",
        "email": "1@2.de",
        "username": "2",
        "password_hash":"d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
        "created_poject_pids": [
            "6055c6a0b58a129e10222bf9",
            "6055c6a0b58a129e10222bf8"
        ],
        "collab_poject_pids": [],
        "default_editor": True
    }
]

mock_project_data = [
    {
        "_id":"6055c6a0b58a129e10222bf7",
        "name":"main",
        "dids":[
            "6055c6a0b58a129e10222bf8"
        ],
        "folders":[],
        "images":[]
    },
    {
        "_id":"6055c6a0b58a129e10222bf8",
        "name":"test project 1",
        "dids":[
            "6055c6a0b58a129e10222bf9"
        ],
        "folders":[],
        "images":[]
    },
    {
        "_id":"6055c6a0b58a129e10222bf9",
        "name":"super nice",
        "dids":[
            "6055c6a0b58a129e10222bg1"
        ],
        "folders":[],
        "images":[]
    }
]

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
        print(e)
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
                'text': {
                    "0000-1616234144": 
                    [
                        ["0001-1616266858730", "a"],
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

@app.route('/userdata', methods=['GET'])
def get_user_data_REST():
    output = None

    try:
        output = []
        if 'uid' in request.args:
            uid = request.args['uid']
        else:
            return {
                "status": 400,
                "message": "No id field provided. Please specify an id."
            }

        for user in mock_user_data:
            if uid == user['uid']:
                output = user

        return jsonify({
            'message': 'Successfull',
            'status': 200,
            'data': output
        })
    except Exception as e:
        print(e)
        return({
            "status": 401,
            "message": "Error"
        })

@app.route('/projects', methods=['GET'])
def get_project_data_REST():
    output = None

    try:
        output = []
        if 'uid' in request.args:
            uid = request.args['uid']
        else:
            return {
                "status": 400,
                "message": "No id field provided. Please specify an id."
            }
        
        for mock_user in mock_user_data:
            if uid == mock_user['uid']:
                user = mock_user

        for pid in user['created_poject_pids']:
            for project in mock_project_data:
                if pid == project['_id']:
                    output.append(project)

        if output:
            return jsonify({
                "message": "Successful",
                "status": 200,
                "value": output
            })
        else:
            return {
                "message": "No Project was found",
                "status": 404
            }
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong!",
            "status": 400
        }

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
