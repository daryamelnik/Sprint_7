import requests
from .urls import BASE_URL
from .helpers import generate_random_string

def create_courier(payload):
    return requests.post(f'{BASE_URL}/courier', data=payload)

def login_courier(payload):
    return requests.post(f'{BASE_URL}/courier/login', data=payload)

def create_order(payload):
    return requests.post(f'{BASE_URL}/orders', json=payload)

def get_orders():
    return requests.get(f'{BASE_URL}/orders')

def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = create_courier(payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []
