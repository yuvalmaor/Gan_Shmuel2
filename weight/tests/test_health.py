import requests

def test_get_health(client):
    response =  requests.get('http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:8084/health')
    assert response.status_code == 200