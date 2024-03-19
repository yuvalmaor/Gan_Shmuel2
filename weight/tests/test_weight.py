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


