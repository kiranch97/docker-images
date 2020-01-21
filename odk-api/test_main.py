from starlette.testclient import TestClient

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
    assert response.status_code == 200
    assert response.json() == {"code": 2, "message": "Cannot get analysed frames. \
                                Problem with server!", "status": "error"}
