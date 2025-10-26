import pytest
import allure
from helpers import generate_random_string
import api



@allure.feature('Courier Creation')
class TestCourierCreation:

    @allure.story('Create Courier')
    @allure.title('Test successful courier creation')
    def test_create_courier_success(self, courier_creation_fixture):
        response = courier_creation_fixture["response"]
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.story('Create Courier')
    @allure.title('Test creating duplicate couriers')
    def test_create_duplicate_courier_error(self, courier_creation_fixture):
        response = api.create_courier(courier_creation_fixture["payload"])

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

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
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
