from tests.test_env.test_health_point import test_health_endpoint
from tests.test_env.test_trucks import *
port:int = 8089
path:str = "ec2-13-200-131-223.ap-south-1.compute.amazonaws.com:"
routes:list[str] = ["health","providers","truck","rates"]

##create providers

##create 
def main_test_env():
    health_route:str = f"https:{path}/{port}:{routes[0]}"
    test_health_endpoint(health_route)

    truck_route:str = f"https:{path}/{port}:{routes[2]}"
    test_post_existing_truck_endpoint(truck_route) 
    test_post_non_existing_truck_endpoint(truck_route)
    test_post_no_provider_id_given(truck_route)
    test_put_exiting_truck_endpoint(truck_route)
    test_put_non_existing_truck_endpoint(truck_route)
    test_put_non_existing_bad_data_truck_endpoint(truck_route)
    test_put_no_data_given(truck_route)
    test_get_existing_truck_endpoint(truck_route)
    test_get_non_existing_truck_endpoint(truck_route)
    test_get_between_time_parameters_endpoint(truck_route)
    test_get_not_between_time_parameters_endpoint(truck_route)