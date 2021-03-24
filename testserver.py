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
            {
                "pid": "6055c6a0b58a129e10222bf7",
                "name": "main"
            }
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
            {
                "pid": "6055c6a0b58a129e10222bf9",
                "name": "super nice"
            },
            {
                "pid": "6055c6a0b58a129e10222bf8",
                "name": "test project 1"
            }
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
            {
                "did": "6055c6a0b58a129e10222bf8",
                "name": "main.tex"
            }
        ],
        "folders":[],
        "images":[]
    },
    {
        "_id":"6055c6a0b58a129e10222bf8",
        "name":"test project 1",
        "dids":[
            {
                "did": "6055c6a0b58a129e10222bd9",
                "name": "main.tex"
            }
        ],
        "folders":[],
        "images":[]
    },
    {
        "_id":"6055c6a0b58a129e10222bf9",
        "name":"super nice",
        "dids":[
            {
                "did": "6055c6a0b58a129e10222bg1",
                "name": "main.tex"
            }
        ],
        "folders":[],
        "images":[]
    }
]

mock_document_data = [
    {
        "did": "6055c6a0b58a129e10222bd9",
        "name": "main.tex",
        "text": {
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

@app.route('/requests/get_user_data', methods=['GET'])
def get_user_data_REST():
    output = None

    try:
        output = mock_user_data[1]

        return jsonify({
            'message': 'Successfull',
            'value': output
        })
    except Exception as e:
        print(e)
        return({
            "message": "Error"
        })

@app.route('/requests/get_project', methods=['POST'])
def get_project_data_REST():
    output = None

    try:
        pid = request.get_json(force=True).get("pid")
        
        for project in mock_project_data:
            if pid['pid'] == project['_id']:
                output = project

        if output:
            return jsonify({
                "message": "Successful",
                "value": output
            })
        else:
            return {
                "message": "No Project was found"
            }
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong!"
        }

@app.route('/requests/get_document', methods=['POST'])
def get_document_data_REST():
    output = None

    try:
        did = request.get_json(force=True).get("did")
        print(did)

        for document in mock_document_data:
            if did == document['did']:
                output = document

        if output:
            return jsonify({
                'message': 'Successful',
                'value': output
            })
        else:
            return {
                "message": "No Document was found"
            }
    except Exception as e:
        print(e)
        return {
            "message": "Something went wrong!"
        }

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
