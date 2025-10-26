import pytest
import allure
from helpers import generate_random_string
import api

@pytest.fixture(scope='function')
def courier_creation_fixture():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = api.create_courier(payload)
    
    yield { "payload": payload, "response": response }

    login_payload = {
        "login": payload["login"],
        "password": payload["password"]
    }

    login_response = api.login_courier(login_payload)
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        api.delete_courier(courier_id)
