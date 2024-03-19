import pytest
import requests
import datetime

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

def test_post_weight_in_and_out(remote_address, in_payload, out_payload):
    in_response = requests.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    out_response = requests.post(remote_address+"/weight", json=out_payload)
    assert out_response.status_code == 200
    assert {
        "bruto": 10000,
        "neto": 1300,
        "truck": "77-777-77",
        "truckTara": 3000
    }.items() <= out_response.json.items()
    
 

def test_post_weight_in_and_in_no_force(remote_address, in_payload):
    in_response = requests.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    in_response = requests.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 400


def test_in_in_with_force(remote_address, in_payload, in_force_payload):
    in_response = requests.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    force_in_response = requests.post(remote_address+"/weight", json=in_force_payload)
    assert force_in_response.status_code == 200
    assert {
        "bruto": 5000,
        "truck": "77-777-77"
    }.items() <= force_in_response.json.items()
    assert in_response.json["id"] == force_in_response.json["id"]

def test_in_out_out_force( remote_address,in_payload, out_payload, out_force_payload):
    test_post_weight_in_and_out( remote_address, in_payload, out_payload)
    response = requests.post(remote_address + 'weight')
    assert response.status_code == 200
    assert {
        "bruto": 10000,
        "neto": 2300,
        "truck": "77-777-77",
        "truckTara": 2000
    }.items() <= response.json.items()


def test_in_and_none(remote_address, in_payload, none_payload):
    in_response = requests.post(remote_address+"/weight", json=in_payload)
    assert in_response.status_code == 200
    assert {
        "bruto": 10000,
        "truck": "77-777-77"
    }.items() <= in_response.json.items()

    none_response = requests.post(remote_address+"/weight", json=none_payload)
    assert none_response.status_code == 400    

def test_register_none_direction(remote_address, none_payload):
    none_response = requests.post(remote_address+"/weight", json=none_payload)
    assert none_response.status_code == 200
    assert {
        "bruto": 220,
        "truck": "na"
    }.items() <= none_response.json.items()
    assert none_response.status_code == 200    

def test_get_weights_with_both_parameters(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&to=20240318235959&filter=in')
    assert response.status_code == 200

def test_get_weights_without_from_parameter(remote_address):
    response = requests.get(remote_address + '/weight?to=20240319235959&filter=out')
    assert response.status_code == 200

def test_get_weights_without_to_parameter(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&filter=none')
    assert response.status_code == 200

def test_get_weights_without_parameters(remote_address):
    response = requests.get(remote_address + '/weight?&filter=out')
    assert response.status_code == 200

def test_get_weights_without_filters(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&to=20240319235959')
    assert response.status_code == 200

def test_get_weights_without_filters_key(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&to=20240319235959&filter=')
    assert response.status_code == 200

def test_get_weights_with_multiple_filters(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&to=20240319235959&filter=in,out,none')
    assert response.status_code == 400

def test_get_weights_with_wrong_filter(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000&to=20240319235959&filter=oumlmls')
    assert response.status_code == 400

def test_get_weights_with_wrong_time(remote_address):
    response = requests.get(remote_address + '/weight?from=20240101070000123&to=20240319235959&filter=in')
    assert response.status_code == 400

def test_get_batch(remote_address):
    file_name = 'containers3.csv'
    response = requests.post(remote_address + '/batch',
                             json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_cvs_not_exists(remote_address):
    file_name = 'containers4.csv'
    response = requests.post(remote_address + '/batch',
                             json={'file': file_name})
    assert response.status_code == 404
    assert response.json == {
        'error': 'File containers4.csv not found in the ./in folder'}

def test_get_batch_filekey_is_not_in_request(remote_address):
    response = requests.post(remote_address+'/batch', json={})
    assert response.status_code == 400
    json_data = response.json()
    assert json_data == {'error': 'No file specified in the request body'}

def test_get_batch_empty_filename(remote_address):
    response = requests.post(remote_address+'/batch', json={'file': ''})
    assert response.status_code == 400
    json_data = response.json()
    assert json_data == {'error': 'The File specified is empty'}

def test_get_batch_with_json_file(remote_address):
    file_name = 'containers4.json'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_csv_missing_containerID(remote_address):
    file_name = 'containers3.csv'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_csv_missing_weight(remote_address):
    file_name = 'containers3.csv'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_json_missing_weight(remote_address):
    file_name = 'containers4.json'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_json_missing_containerID(remote_address):
    file_name = 'containers4.json'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_csv_missing_unit(remote_address):
    file_name = 'containers3.csv'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_get_batch_process_json_missing_unit(remote_address):
    file_name = 'containers4.json'
    response = requests.post(remote_address+'/batch', json={'file': file_name})
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_item(remote_address):
        response = requests.get(remote_address+'/item/CONT-00001')
        assert response.status_code == 200
        # Test for valid JSON response
        json_data = response.json
        assert isinstance(json_data, dict)
        assert 'id' in json_data
        assert 'tara' in json_data
        assert 'sessions' in json_data
        default_from_str = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y%m%d%H%M%S')
        default_to_str = datetime.now().strftime('%Y%m%d%H%M%S')
        # Test for invalid date format
        response = requests.get(remote_address+'/item/CONT-00001?from=20220101120000&to=2022010123000')
        assert response.status_code == 400
        assert 'error' in response.json
        # Test for non-existing item
        response = requests.get(remote_address+'/item/non_existing_id')
        assert response.status_code == 404
        assert 'error' in response.json





