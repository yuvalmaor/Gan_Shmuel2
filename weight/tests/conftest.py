import pytest
from src.app import create_app
from src.database import db
from src.models import Transaction, Container
from datetime import datetime
from requests import Session
containers_data = [
    {"container_id": "CONT-00001", "weight": 2000, "unit": "kg"},
    {"container_id": "CONT-00002", "weight": 1500, "unit": "kg"},
    {"container_id": "CONT-00003", "weight": 1000, "unit": "lbs"},
    {"container_id": "CONT-00004", "weight": None, "unit": None},
    {"container_id": "CONT-00005", "weight": 2200, "unit": "kg"},
    {"container_id": "CONT-00006", "weight": 2000, "unit": "lbs"},
    {"container_id": "CONT-00007", "weight": None, "unit": None},
]

transactions_data = [
    # Truck 1 enters with a container, starts a new session
    {"datetime": datetime.now(), "direction": "in", "truck": "TRUCK001", "containers": "CONT-00001",
        "bruto": 5000, "truckTara": None, "neto": None, "produce": "orange", "session_id": 1},
    # Truck 1 leaves, concluding its session
    {"datetime": datetime.now(), "direction": "out", "truck": "TRUCK001", "containers": "na",
        "bruto": 5000, "truckTara": 2000, "neto": 1000, "produce": "", "session_id": 1},
    # Standalone container weighing
    {"datetime": datetime.now(), "direction": "none", "truck": "na", "containers": "CONT-00002",
        "bruto": 1500, "truckTara": None, "neto": None, "produce": "na", "session_id": 4},
    # Truck 2 enters without a container, starts a new session
    {"datetime": datetime.now(), "direction": "in", "truck": "TRUCK002", "containers": "ONT-00002,ONT-00003",
        "bruto": 15000, "truckTara": None, "neto": None, "produce": "apples,oranges", "session_id": 2},
    # Truck 2 leaves, but no containers were registered
    {"datetime": datetime.now(), "direction": "out", "truck": "TRUCK002", "containers": "na",
        "bruto": 15000, "truckTara": 5000, "neto": 7500, "produce": "na", "session_id": 2},
    # More transactions follow the pattern
    # A new truck enters with multiple containers
    {"datetime": datetime.now(), "direction": "in", "truck": "TRUCK003", "containers": "CONT-00003,CONT-00004",
        "bruto": 10000, "truckTara": None, "neto": None, "produce": "tomato", "session_id": 3},
    # Truck 3 leaves with those containers, completing the transaction
    {"datetime": datetime.now(), "direction": "out", "truck": "TRUCK003", "containers": "",
        "bruto": 10000, "truckTara": 2000, "neto": "na", "produce": "", "session_id": 3},
]

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.config.update({
        "TESTING": True,
    })
    with app.app_context():
        db.create_all()

        for container_data in containers_data:
            container = Container(**container_data)
            db.session.add(container)

        for transaction_data in transactions_data:
            transaction = Transaction(**transaction_data)
            db.session.add(transaction)

        db.session.commit()
     

    yield app

@pytest.fixture()
def client():
    with Session() as s:
        yield s


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
    
@pytest.fixture()
def remote_address():
    return 'http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:8084'
