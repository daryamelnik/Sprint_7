import pytest
import allure
from helpers import generate_random_string
import api

@allure.feature('Courier Login')
class TestCourierLogin:

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
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.story('Login Courier')
    @allure.title('Test courier login with missing login')
    def test_login_courier_missing_login_error(self, courier_creation_fixture):
        payload = {
            "password": courier_creation_fixture["payload"]["password"]
        }

        response = api.login_courier(payload)
    
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.story('Login Courier')
    @allure.title('Test courier login with missing password')
    def test_login_courier_missing_password_error(self, courier_creation_fixture):
        payload = {
            "login": courier_creation_fixture["payload"]["login"],
            "password": ""
        }

        response = api.login_courier(payload)
    
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.story('Login Courier')
    @allure.title('Test courier login with non-existent user')
    def test_login_non_existent_user_error(self):
        payload = {
            "login": "non_existent_user",
            "password": "password"
        }

        response = api.login_courier(payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
