import os
import pytest
from src.app import create_app
from src.routes.batch import *
from src.database import db
from src.models import Transaction, Container
from datetime import datetime

def test_process_csv(client, app):
    file_name = 'containers3.csv'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_csv_not_exists(client, app):
    file_name = 'containers4.csv'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 404
    assert response.json == {'error': 'File containers4.csv not found in the ./in folder'}

def test_process_filekey_not_in_request(client, app):
    response = client.post('/batch', json={})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data == {'error': 'No file specified in the request body'}

def test_process_batch_empty_filename(client, app):
    response = client.post('/batch', json={'file': ''})
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data == {'error': 'The File specified is empty'}

def test_process_batch_with_json_file(client, app):
    file_name = 'containers4.json'  
    response = client.post('/batch', json={'file': file_name})
    print("Response Data:", response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_csv_missing_containerID(client, app):
    file_name = 'containers3.csv'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_csv_missing_weight(client, app):
    file_name = 'containers3.csv'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_json_missing_weight(client, app):
    file_name = 'containers4.json'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_json_missing_containerID(client, app):
    file_name = 'containers4.json'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_csv_missing_unit(client, app):
    file_name = 'containers3.csv'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}

def test_process_json_missing_unit(client, app):
    file_name = 'containers4.json'
    response = client.post('/batch', json={'file': file_name})
    print(response.data)
    with app.app_context():
        containers = Container.query.all()
        for container in containers:
            print(f"<Container {container.container_id}, Weight: {container.weight} {container.unit}>")
    assert response.status_code == 200
    assert response.json == {'message': 'Batch processing completed'}




   