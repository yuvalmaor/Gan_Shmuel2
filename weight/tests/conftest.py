import pytest

@pytest.fixture()
def remote_address():
    return 'http://ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:8084'