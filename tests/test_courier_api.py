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

    @allure.story('Login Courier')
    @allure.title('Test successful courier login')
    def test_login_courier_success(self):
        credentials = api.register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }

        response = api.login_courier(payload)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.story('Login Courier')
    @allure.title('Test courier login with incorrect credentials')
    def test_login_courier_incorrect_credentials_error(self):
        credentials = api.register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": "incorrect_password"
        }

        response = api.login_courier(payload)

        assert response.status_code == 404

    @allure.story('Login Courier')
    @allure.title('Test courier login with missing required fields')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field_error(self, missing_field):
        credentials = api.register_new_courier_and_return_login_password()
        payload = {
            "login": credentials[0],
            "password": credentials[1]
        }
        if missing_field == "password":
            payload[missing_field] = ""
        else:
            del payload[missing_field]

        response = api.login_courier(payload)
    
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text

    @allure.story('Login Courier')
    @allure.title('Test courier login with non-existent user')
    def test_login_non_existent_user_error(self):
        payload = {
            "login": "non_existent_user",
            "password": "password"
        }

        response = api.login_courier(payload)

        assert response.status_code == 404
