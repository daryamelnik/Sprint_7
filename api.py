import allure
import requests
from urls import BASE_URL
from helpers import generate_random_string

@allure.step('Create a courier')
def create_courier(payload):
    return requests.post(f'{BASE_URL}/courier', data=payload)

@allure.step('Login a courier')
def login_courier(payload):
    return requests.post(f'{BASE_URL}/courier/login', data=payload)

@allure.step('Create an order')
def create_order(payload):
    return requests.post(f'{BASE_URL}/orders', json=payload)

@allure.step('Get orders')
def get_orders():
    return requests.get(f'{BASE_URL}/orders')

@allure.step('Delete a courier')
def delete_courier(courier_id):
    return requests.delete(f'{BASE_URL}/courier/{courier_id}')

@allure.step('Register a new courier and return login and password')
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
