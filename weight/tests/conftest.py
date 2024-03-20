import pytest
import logging

@pytest.fixture()
def remote_address():
    return 'http://localhost:8084'

@pytest.fixture()
def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers= [
                        logging.FileHandler("logs/weight-tests-logs.txt"),
                        ])
    logger = logging.getLogger(__name__)
    return logger