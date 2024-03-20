import requests

# from ... import db, app, logger

# port: int = 5000
# path: str = "localhost"
port: int = 8089
path: str = "ec2-13-200-131-223.ap-south-1.compute.amazonaws.com"
routes: list[str] = ["health", "providers", "truck", "rates"]

health_route: str = f"http://{path}:{port}/{routes[0]}"
truck_route: str = f"http://{path}:{port}/{routes[2]}"


def test_health_endpoint():
    response = requests.get(health_route)
    assert response.status_code == 200
    # assert response == "OK"


url = truck_route


# POST /truck - registers a truck in the system
# def test_post_existing_truck_endpoint():
#     existing_truck_id = "222-33-111"
#     data = {"provider": 1, "id": existing_truck_id}
#     response = requests.post(url, json=data)
#     assert response.status_code == 400
#     assert response.json() == {
#         "message": f"Truck with ID {existing_truck_id} already exists in the database."
#     }


def test_post_no_provider_id_given():
    data = {"provider": 1}  # Missing id field
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert response.json() == {"message": "Missing required fields. Truck not saved."}


def test_post_truck_missing_required_fields():
    data = {}  # Missing provider and ID
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert response.json() == {"message": "Missing required fields. Truck not saved."}


# def test_post_non_existing_provider_id():
#     non_existing_provider_id = 999
#     data = {"provider": non_existing_provider_id, "id": "222-33-111"}
#     response = requests.post(url, json=data)
#     assert response.status_code == 404
#     assert response.json() == {
#         "message": f"Provider with ID {non_existing_provider_id} does not exist. Truck not saved."
#     }


# def test_post_truck_with_invalid_id():
#     invalid_id = "abc123"  # Invalid ID (string)
#     data = {"provider": 1, "id": invalid_id}
#     response = requests.post(url, json=data)
#     assert response.status_code == 400
#     assert response.json() == {"message": "Truck ID must be an integer."}
#     print("test_post_truck_with_invalid_id OK")


# def test_post_truck_successful():
#     provider_id = 1  # Assuming a valid provider ID
#     truck_id = "ABC-123"
#     response = requests.post(url, json={"provider": provider_id, "id": truck_id})
#     assert response.status_code == 201
#     assert (
#         response.json()["message"]
#         == f"Truck with ID {truck_id} registered successfully."
#     )
#     print("test_post_truck_successful OK")


# def test_put_exiting_truck_endpoint(url):
#     # Assuming 'id' exists in the database and valid 'provider_id' provided
#     truck_id = 11
#     data = {"provider_id": "222"}
#     response = requests.put(f"{url}/{truck_id}", json=data)
#     assert response.status_code == 200


# def test_put_non_existing_truck_endpoint(url):
#     # Assuming 'id' does not exist in the database
#     truck_id = 20
#     data = {"provider_id": "abc"}
#     response = requests.put(f"{url}/{truck_id}", json=data)
#     assert response.status_code == 404
#     # Add more assertions as needed to verify the response content


# def test_put_non_existing_bad_data_truck_endpoint(url):
#     # Assuming 'id' does not exist in the database
#     truck_id = 20
#     new_provider_id = "12"
#     data = {"provider_id": new_provider_id}
#     response = requests.put(f"{url}/{truck_id}", json=data)
#     assert response.status_code == 404
#     # Add more assertions as needed to verify the response content


# def test_put_no_data_given(url):
#     data = {}
#     response = requests.put(url, json=data)
#     assert response.status_code == 400


# def test_get_existing_truck_endpoint(url):
#     pass


# def test_get_non_existing_truck_endpoint(url):
#     pass


# def test_get_between_time_parameters_endpoint(url):
#     pass


# def test_get_not_between_time_parameters_endpoint(url):
#     pass
