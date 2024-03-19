from test_health_point import test_health_endpoint
from test_trucks import *
import requests

# python tests/test_env/test_env.py

port: int = 8084
path: str = "ec2-13-200-131-223.ap-south-1.compute.amazonaws.com"
# path: str = "localhost"
routes: list[str] = ["health", "providers", "truck", "rates"]

##create providers


##create
def main_test_env():
    health_route: str = f"http://{path}:{port}/{routes[0]}"
    test_health_endpoint(health_route)
    truck_route: str = f"http://{path}:{port}/{routes[2]}"
    test_post_existing_truck_endpoint(truck_route)
    test_post_no_provider_id_given(truck_route)
    test_post_non_existing_provider_id(truck_route)
    test_post_truck_missing_required_fields(truck_route)
