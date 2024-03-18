import requests

def test_post_existing_truck_endpoint(url):
    data = {"provider_id": "11", "id": "111"}
    response = requests.post(url, json=data)
    assert response.status_code == 200

def test_post_non_existing_truck_endpoint(url):
    data = {"provider_id": "11", "id": "111"}
    response = requests.post(url, json=data)
    assert response.status_code == 400

def test_post_no_provider_id_given(url):
     data = {}
     response = requests.post(url, json=data)
     assert response.status_code == 400

def test_put_exiting_truck_endpoint(url):
    # Assuming 'id' exists in the database and valid 'provider_id' provided
    truck_id = 11
    data = {"provider_id": "222"}
    response = requests.put(f"{url}/{truck_id}", json=data)
    assert response.status_code == 200

def test_put_non_existing_truck_endpoint(url):
    # Assuming 'id' does not exist in the database
    truck_id = 20
    data = {"provider_id": "abc"}
    response = requests.put(f"{url}/{truck_id}", json=data)
    assert response.status_code == 404
    # Add more assertions as needed to verify the response content

def test_put_non_existing_bad_data_truck_endpoint(url):
    # Assuming 'id' does not exist in the database
    truck_id = 20
    new_provider_id = "12"
    data = {"provider_id": new_provider_id}
    response = requests.put(f"{url}/{truck_id}", json=data)
    assert response.status_code == 404
    # Add more assertions as needed to verify the response content

def test_put_no_data_given(url):
     data = {}
     response = requests.put(url, json=data)
     assert response.status_code == 400

def test_get_existing_truck_endpoint(url):
    pass

def test_get_non_existing_truck_endpoint(url):
    pass

def test_get_between_time_parameters_endpoint(url):
    pass
    
def test_get_not_between_time_parameters_endpoint(url):
    pass