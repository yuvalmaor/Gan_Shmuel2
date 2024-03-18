import pytest
from ..src.app import create_app
from ..src.database import db

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    
    with app.app_context():
        db.create_all()
        
    yield app