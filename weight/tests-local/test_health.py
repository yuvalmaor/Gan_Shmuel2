def test_get_health(client, remote_address):
    response =  client.get(remote_address + '/health')
    assert response.status_code == 200