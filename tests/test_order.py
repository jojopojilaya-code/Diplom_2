import pytest
import allure
from data import *
from helpers import *
from methods.order_methods import OrderMethods


class TestOrderCreate:

    @pytest.mark.parametrize("ingredient_count", [2, 3, 5], ids=["2_ingredients", "3_ingredients", "5_ingredients"])
    @allure.title('Позитивный сценарий: создание заказа с авторизацией (ингредиентов: {ingredient_count})')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_authorized_valid_ingredients_success(self, authorization_user, ingredients, ingredient_count):
        user_data = authorization_user
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:ingredient_count]]
        status_code, response = OrderMethods().post_create_order_with_token(
            accessToken=user_data["accessToken"],
            json={"ingredients": valid_ingredients}
        )
        assert all([
            status_code == 200,
            response["success"] is True,
            "order" in response,
            "name" in response
        ]), (
            f"Ошибка создания заказа.\n"
            f"Статус: {status_code} (ожидалось 200).\n"
            f"Success: {response.get('success')} (ожидалось True).\n"
            f"Наличие номера заказа: {'order' in response} (ожидалось True).\n\n"
            f"Полный ответ: {response}\n"
        )
        

    @pytest.mark.parametrize("ingredient_count", [2, 3, 5], ids=["2_ingredients", "3_ingredients", "5_ingredients"])
    @allure.title('Попытка создания заказа без авторизации (ингредиентов: {ingredient_count})')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_unauthorized_valid_ingredients_success(self, ingredients, ingredient_count):
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:ingredient_count]]
        status_code, response = OrderMethods().post_create_order_no_token(
            json={"ingredients": valid_ingredients}
        )
        assert all([
            status_code == 200,
            response["success"] is True,
            "order" in response,
            "name" in response
        ]), (
            f"Ошибка создания заказа без авторизации.\n"
            f"Статус: {status_code} (ожидалось 200).\n"
            f"Success: {response.get('success')} (ожидалось True).\n"
            f"Наличие номера заказа: {'order' in response} (ожидалось True).\n\n"
            f"Полный ответ: {response}\n"
        )


    @pytest.mark.parametrize("invalid_data", INVALID_ORDER_DATA, ids=lambda x: x[1]) 
    @allure.title('Негативный сценарий: создание заказа с авторизацией и невалидными ингредиентами ({invalids[1]})')
    @allure.description('ОР: Система возвращает ошибку 500 Internal Server Error')
    def test_create_order_authorized_invalid_ingredients(self, authorization_user, invalid_data):
        user_data = authorization_user
        invalid_ingredients, test_id = invalid_data      
        status_code, response_text = OrderMethods().post_create_order_with_token(
            accessToken=user_data["accessToken"],
            json={"ingredients": invalid_ingredients}
        )       
        assert status_code == 500, (
            f"Ожидался статус 500, получен {status_code}\n"
            f"Тип невалидных данных: {test_id}\n"
            f"Использованные ингредиенты: {invalid_ingredients}\n"
            f"Ответ сервера: {response_text[:200]}..."
    )
        

    @allure.title('Негативный сценарий: создание заказа без ингредиентов')
    @allure.description('ОР: Система возвращает ошибку 400 Bad Request')
    def test_create_order_no_ingredients_error(self, authorization_user):
        user_data = authorization_user
        status_code, response = OrderMethods().post_create_order_with_token(
            accessToken=user_data["accessToken"],
            json={"ingredients": []}
        )   
        assert all([
            status_code == 400,
            response["success"] is False,
            response["message"] == NO_INGREDIENTS
        ]), (
            f"Ошибка проверки отсутствия ингредиентов.\n"
            f"Статус: {status_code} (ожидалось 400).\n"
            f"Сообщение: '{response.get('message')}'\n"
            f"(ожидалось '{NO_INGREDIENTS}').\n\n"
            f"Полный ответ: {response}\n"
        )


class TestGetOrder:

    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('ОР: Возвращается список заказов пользователя со статусом 200')
    def test_get_user_orders_authorized_success(self, authorization_user, ingredients):
        user_data = authorization_user
        ingredient_hashes = [ingredients[0]["_id"], ingredients[1]["_id"]]
        OrderMethods().post_create_order_with_token(
            accessToken=user_data["accessToken"],
            json={"ingredients": ingredient_hashes}
        )     
        status_code, response = OrderMethods().get_order_with_token(
            accessToken=user_data["accessToken"]
        )        
        assert all([
            status_code == 200,
            response["success"] is True,
            isinstance(response["orders"], list),
            "total" in response,
            "totalToday" in response
        ]), (
            f"Ошибка получения заказов.\n"
            f"Статус: {status_code} (ожидалось 200).\n"
            f"Success: {response.get('success')} (ожидалось True).\n"
            f"Наличие списка заказов: {isinstance(response.get('orders'), list)} (ожидалось True).\n\n"
            f"Полный ответ: {response}"
        )


    @allure.title('Попытка получения заказов неавторизованного пользователя')
    @allure.description('ОР: Возвращается ошибка 401 Unauthorized')
    def test_get_user_orders_unauthorized_fail(self):
        status_code, response = OrderMethods().get_order_no_token()    
        assert all([
            status_code == 401,
            response["success"] is False,
            response["message"] == AUTH_REQUIRED
        ]), (
            f"Ошибка проверки авторизации.\n"
            f"Статус: {status_code} (ожидалось 401).\n"
            f"Сообщение: '{response.get('message')}'\n"
            f"(ожидалось '{AUTH_REQUIRED}').\n\n"
            f"Полный ответ: {response}"
        )


    @allure.title('Получение пустого списка заказов нового пользователя')
    @allure.description('ОР: Возвращается пустой массив заказов')
    def test_get_empty_user_orders_success(self, authorization_user):
        user_data = authorization_user      
        status_code, response = OrderMethods().get_order_with_token(
            accessToken=user_data["accessToken"]
        )        
        assert all([
            status_code == 200,
            response["success"] is True,
            len(response["orders"]) == 0  
        ]), (
            f"Ошибка проверки пустого списка заказов.\n"
            f"Статус: {status_code} (ожидалось 200).\n"
            f"Количество заказов: {len(response.get('orders'))} (ожидалось 0).\n\n"
            f"Полный ответ: {response}"
        )
    