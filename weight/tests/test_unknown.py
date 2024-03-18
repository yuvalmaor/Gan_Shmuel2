def test_get_unknown(client):
    response = client.get("/unknown")

    expected_response = [
        "CONT-00004",
        "CONT-00007"
    ]
    response_data = response.json

    assert response.status_code == 200
    assert expected_response == response_data
