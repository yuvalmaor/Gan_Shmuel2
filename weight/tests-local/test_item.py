from src.models import Container,Transaction
from src.database import db
from datetime import datetime

def test_item(client,remote_address):
    with client:
        response = client.get('/item/Container1')
        assert response.status_code == 200

        # Test for valid JSON response
        json_data = response.json
        assert isinstance(json_data, dict)
        assert 'id' in json_data
        assert 'tara' in json_data
        assert 'sessions' in json_data

        default_from_str = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y%m%d%H%M%S')
        default_to_str = datetime.now().strftime('%Y%m%d%H%M%S')
        assert json_data['from'] == default_from_str
        assert json_data['to'] == default_to_str

        # Test for invalid date format
        response = client.get('/item/1?from=20220101120000&to=2022010123000')
        assert response.status_code == 400
        assert 'error' in response.json

        # Test for non-existing item
        response = client.get('/item/non_existing_id')
        assert response.status_code == 404
        assert 'error' in response.json