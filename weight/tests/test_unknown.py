from src.models import Container
from src.database import db


def test_get_unknown(client):
    response = client.get("/unknown")

    expected_response = [
        "CONT-00004",
        "CONT-00007"
    ]
    response_data = response.json

    assert response.status_code == 200
    assert expected_response == response_data


def test_get_unknown_empty_database(app, client):
    with app.app_context():
        Container.query.delete()
        db.session.commit()

    response = client.get("/unknown")

    expected_response = []
    response_data = response.json

    assert response.status_code == 200
    assert expected_response == response_data
