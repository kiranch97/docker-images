import os
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

#os.environ['DATABASE_CONNECTION_STRING'] = 'sqlite:///'
#os.environ['RMQ_USER'] = '<>'
#os.environ['RMQ_PASSWORD'] = '<>'
#os.environ['RMQ_URL'] = '<>'

from main import app

client = TestClient(app)

def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "odk-video.stadswerken.amsterdam", "status": "succes"}

def test_get_detected_objects_no_app_id():
    response = client.get("/detected_objects?day=1")
    assert response.status_code == 422

def test_get_detected_objects_no_day():
    response = client.get("/detected_objects?app_id=1")
    assert response.status_code == 422

def test_get_detected_objects_invalid_data():
    response = client.get("/detected_objects?app_id=1&day=1")
    assert response.status_code == 500
    assert response.json() == {"code": 2, "message": "Cannot get analysed frames. \
                                Problem with server!", "status": "error"}

def test_last_analysed_frames():
    response = client.get("/last_analysed_frames?app_id=1")
    assert response.status_code == 200
    assert response.json() == None

def test_dash_stream_devices():
    response = client.get("/dash_stream_devices?app_id=1&day=1")
    assert response.status_code == 500
    assert response.json() == {"code": 2, "message": "Cannot get analysed frames. \
                                Problem with server!", "status": "error"}

def test_dash_total():
    response = client.get("/dash_total?day=1")
    assert response.status_code == 500
    assert response.json() == {"code": 2, "message": "Cannot get analysed frames. \
                                Problem with server!", "status": "error"}

def test_dash_map_data():
    response = client.get("/dash_map_data?day=1")
    assert response.status_code == 500
    assert response.json() == {"code": 2, "message": "Cannot get analysed frames. \
                                Problem with server!", "status": "error"}

"""
Test the websocket without setting the connection. It should return: Not available
"""
def test_stream():
    client = TestClient(app)
    with client.websocket_connect("/stream") as websocket:
        # trigger the message queue by sending it a message
        websocket.send_json({"img": "Hello WebSocket"})
        # wait for response
        assert websocket.receive_json() == {"error": "MessageServer Not Available"}

