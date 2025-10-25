import requests
import pytest
import allure
from .helpers import generate_random_string, register_new_courier_and_return_login_password, BASE_URL

@allure.feature('Courier API')
class TestCourierAPI:

    @allure.story('Create Courier')
    @allure.title('Test successful courier creation')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.story('Create Courier')
    @allure.title('Test creating duplicate couriers')
    def test_create_duplicate_courier_error(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        requests.post(f'{BASE_URL}/courier', data=payload)
        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @allure.story('Create Courier')
    @allure.title('Test creating courier with missing required fields')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_error(self, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        del payload[missing_field]

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text

    @allure.story('Login Courier')
    @allure.title('Test successful courier login')
    def test_login_courier_success(self):
        credentials = register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.story('Login Courier')
    @allure.title('Test courier login with incorrect credentials')
    def test_login_courier_incorrect_credentials_error(self):
        credentials = register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": "incorrect_password"
        }

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        assert response.status_code == 404

    @allure.story('Login Courier')
    @allure.title('Test courier login with missing required fields')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field_error(self, missing_field):
        credentials = register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        if missing_field == "password":
            payload[missing_field] = ""
        else:
            del payload[missing_field]

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text

    @allure.story('Login Courier')
    @allure.title('Test courier login with non-existent user')
    def test_login_non_existent_user_error(self):
        payload = {
            "login": "non_existent_user",
            "password": "password"
        }

        response = requests.post(f'{BASE_URL}/courier/login', data=payload)

        assert response.status_code == 404

@allure.feature('Order API')
class TestOrderAPI:

    @allure.story('Create Order')
    @allure.title('Test successful order creation')
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_success(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, 106",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }

        response = requests.post(f'{BASE_URL}/orders', json=payload)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.story('Get Orders')
    @allure.title('Test getting the list of orders')
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/orders')
        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)
