import os
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

os.environ['RMQ_USER'] = 'test'
os.environ['RMQ_PASSWORD'] = 'test'
os.environ['RMQ_URL'] = 'localhost'

from main import app

client = TestClient(app)

"""
Test the websocket with faulty connection. It should return: No access
"""
def test_stream_rmq_not_allowed():
    client = TestClient(app)
    with client.websocket_connect("/stream") as websocket:
        # trigger the message queue by sending it a message
        websocket.send_json({"img": "Hello WebSocket"})
        # wait for response
        assert websocket.receive_json() == {"error": "MessageServer Not Available"}

