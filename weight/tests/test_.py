import requests


def test_get_health(remote_address):
    response = requests.get(remote_address + '/health')
    assert response.status_code == 200


def test_get_unknown(remote_address):
    response = requests.get(remote_address + '/unknown')
    assert response.status_code == 200


def test_get_session(remote_address):
    response = requests.get(remote_address + '/session/aa')

    expected_response = {"error": "Session not found"}
    response_data = response.json

    assert response.status_code == 404
    assert expected_response == response_data

# def test_get_batch(remote_address):
  
  
