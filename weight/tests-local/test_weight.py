import pytest
from src.app import create_app
from src.database import db
from src.models import Transaction, Container
from datetime import datetime


def test_get_weights_with_both_parameters(client):
    response = client.get('/weight?from=20240101070000&to=20240318235959&filter=in')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list)  

def test_get_weights_without_from_parameter(client):
    response = client.get('/weight?to=20240319235959&filter=out')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list) 

def test_get_weights_without_to_parameter(client):
    response = client.get('/weight?from=20240101070000&filter=none')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list)

def test_get_weights_without_parameters(client):
    response = client.get('/weight?&filter=out')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list)

def test_get_weights_without_filters(client):
    response = client.get('/weight?from=20240101070000&to=20240319235959')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list)  

def test_get_weights_without_filters_key(client):
    response = client.get('/weight?from=20240101070000&to=20240319235959&filter=')
    assert response.status_code == 400
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, dict)  

def test_get_weights_with_multiple_filters(client):
    response = client.get('/weight?from=20240101070000&to=20240319235959&filter=in,out,none')
    assert response.status_code == 200
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, list)

def test_get_weights_with_wrong_filter(client):
    response = client.get('/weight?from=20240101070000&to=20240319235959&filter=oumlmls')
    assert response.status_code == 400
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, dict)

def test_get_weights_with_wrong_time(client):
    response = client.get('/weight?from=20240101070000123&to=20240319235959&filter=in')
    assert response.status_code == 400
    json_data = response.json
    print(json_data) 
    assert isinstance(json_data, dict)

@pytest.fixture()
def in_payload():
    return {
    "direction": "in",
    "truck" : "77-777-77",
    "containers" : "CONT-00001,CONT-00002,CONT-00005",
    "unit" : "kg",
    "force" : False,
    "produce": "apples",
    "weight": 10000
}

@pytest.fixture()
def in_force_payload():
    return {
    "direction": "in",
    "truck" : "77-777-77",
    "containers" : "CONT-00001,CONT-00002,CONT-00005",
    "unit" : "kg",
    "force" : True,
    "produce": "apples",
    "weight": 5000
}

@pytest.fixture()
def out_payload():
    return {
    "direction": "out",
    "truck" : "77-777-77",
    "unit" : "kg",
    "force" : False,
    "produce": "apples",
    "weight": 3000
}

@pytest.fixture()
def out_force_payload():
    return {
    "direction": "out",
    "truck" : "77-777-77",
    "unit" : "kg",
    "force" : True,
    "produce": "apples",
    "weight": 2000
}

@pytest.fixture()
def none_payload():
    return {
    "direction": "none",
    "truck" : "na",
    "containers" : "Container60",
    "unit" : "kg",
    "force" : False,
    "produce": "na",
    "weight": 220
}




def test_post_weight_in_and_out(client,remote_address, in_payload, out_payload):
    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    out_response = client.post(remote_address+"/weight", json=out_payload)
    assert out_response.status_code == 200
    assert {
        "bruto": 10000,
        "neto": 1300,
        "truck": "77-777-77",
        "truckTara": 3000
    }.items() <= out_response.json.items()
    
 

def test_post_weight_in_and_in_no_force(client,remote_address, in_payload):
    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 400


def test_in_in_with_force(client,remote_address, in_payload, in_force_payload):
    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    force_in_response = client.post(remote_address+"/weight", json=in_force_payload)
    assert force_in_response.status_code == 200
    assert {
        "bruto": 5000,
        "truck": "77-777-77"
    }.items() <= force_in_response.json.items()
    assert in_response.json["id"] == force_in_response.json["id"]

def test_in_out_out_force(client, remote_address,in_payload, out_payload, out_force_payload):
    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    out_response = client.post(remote_address+"/weight", json=out_payload)
    assert out_response.status_code == 200
    assert {
        "bruto": 10000,
        "neto": 1300,
        "truck": "77-777-77",
        "truckTara": 3000
    }.items() <= out_response.json.items()
    force_out_response = client.post(remote_address + '/weight', json=out_force_payload)
    assert force_out_response.status_code == 200
    assert {
        "bruto": 10000,
        "neto": 2300,
        "truck": "77-777-77",
        "truckTara": 2000
    }.items() <= force_out_response.json.items()
    assert out_response.json["id"] == force_out_response.json["id"]
 


def test_in_and_none(client,remote_address, in_payload, none_payload):
    in_response = client.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    none_response = client.post(remote_address+"/weight", json=none_payload)
    assert none_response.status_code == 400    

def test_register_none_direction(client,remote_address, none_payload):
    none_response = client.post(remote_address+"/weight", json=none_payload)
    assert none_response.status_code == 200
    assert {
        "bruto": 220,
        "truck": "na"
    }.items() <= none_response.json.items()
    assert none_response.status_code == 200

