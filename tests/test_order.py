import pytest
import allure
import api

@allure.feature('Order API')
class TestOrder:

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
