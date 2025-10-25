import pytest
import allure
from .helpers import generate_random_string
from . import api

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

@allure.feature('Courier API')
class TestLoginAPI:

    @allure.story('Login Courier')
    @allure.title('Test successful courier login')
    def test_login_courier_success(self, courier_creation_fixture):
        payload = {
            "login": courier_creation_fixture["payload"]["login"],
            "password": courier_creation_fixture["payload"]["password"]
        }

        response = api.login_courier(payload)

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.story('Login Courier')
    @allure.title('Test courier login with incorrect credentials')
    def test_login_courier_incorrect_credentials_error(self, courier_creation_fixture):
        payload = {
            "login": courier_creation_fixture["payload"]["login"],
            "password": "incorrect_password"
        }

        response = api.login_courier(payload)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @allure.story('Login Courier')
    @allure.title('Test courier login without login field')
    def test_login_courier_missing_login_error(self, courier_creation_fixture):
        payload = {
            "password": courier_creation_fixture["payload"]["password"]
        }

        response = api.login_courier(payload)

        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text

    @allure.story('Login Courier')
    @allure.title('Test courier login without password field')
    def test_login_courier_missing_password_error(self, courier_creation_fixture):
        payload = {
            "login": courier_creation_fixture["payload"]["login"],
            "password": ""
        }

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
        assert "Учетная запись не найдена" in response.text
