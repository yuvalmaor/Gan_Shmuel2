def test_get_session(client):
    response = client.get("/session/1")

    expected_response = { 
        "id": "1",
        "truck": "TRUCK001",
        "bruto": 5000,
        "truckTara": 2000,
        "neto": 1000
    }
    response_data = response.json

    assert response.status_code == 200
    assert expected_response == response_data
