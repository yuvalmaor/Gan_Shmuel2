import requests


def test_health_endpoint(url):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
