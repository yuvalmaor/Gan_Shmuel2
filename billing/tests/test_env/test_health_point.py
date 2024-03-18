import requests

def test_health_endpoint(url):
    response = requests.get(url)
    # Check if the status code is 200
    assert response.status_code == 200
    # Optional: Check if the response body matches expected content
    # For example, if the health check endpoint returns {"status": "up"}
    # you can uncomment the following line to test for that response:
    # assert response.json() == {"status": "up"}