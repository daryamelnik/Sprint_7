import allure
import requests
from .urls import BASE_URL

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