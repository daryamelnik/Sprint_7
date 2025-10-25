import pytest
import allure
from .helpers import generate_random_string
from . import api

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

        response = api.create_courier(payload)

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

        api.create_courier(payload)
        response = api.create_courier(payload)

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

        response = api.create_courier(payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text


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

        response = api.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.story('Get Orders')
    @allure.title('Test getting the list of orders')
    def test_get_orders_list(self):
        response = api.get_orders()
        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)
