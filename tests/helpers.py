import allure
import random
import string
from . import api

@allure.step('Generate a random string')
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

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

    response = api.create_courier(payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []
