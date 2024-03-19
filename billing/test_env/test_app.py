# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import json
# import pytest

# from app import app
# from models import Truck, Provider

# To run:
# PYTHONPATH=<full path of billing directory> pytest tests/test_app.py -v


# @pytest.fixture
# def app():
#     app = app_under_test
#     app_under_test.config.update({
#         "TESTING": True,
#         "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
#     })
#     db = SQLAlchemy(app_under_test)
#     with app_under_test.app_context():
#         db.create_all()
#         yield app_under_test
#         db.drop_all()
# maybe there is another way to create a DB just for testing, Flask can't work with two DB that are configured in SQALchemy.


# @pytest.fixture
# def client():
#     return app.test_client()


# @pytest.fixture
# def runner():
#     return app.test_cli_runner()


# # Example test for the home route
# def test_home(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert b"Hellooooo" in response.data


# # Example test for the healthcheck route
# def test_healthcheck(client):
#     response = client.get("/health")
#     assert response.status_code == 200
#     doc = json.loads(response.data)
#     assert doc["status"] == "ok"
#     assert doc["message"] == "Service is healthy"


# # Example test for the trucks route
# def test_get_trucks_empty_db(client):
#     response = client.get("/trucks")
#     assert response.status_code == 200
#     assert b"[]" in response.data


# # Example test for POST /<provider>
# def test_post_provider(client):
#     response = client.post("/SomeProvider")
#     assert response.status_code == 201
#     assert b'"id"' in response.data


# # # More tests can be added here, following the same pattern
