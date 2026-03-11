import requests
import allure
from data import *
from helpers import *


class OrderMethods:

    @allure.step('Попытка создать заказ НЕ авторизированным пользователем')
    def post_create_order_no_token(self, json):
        response = requests.post(CREATE_ORDER_URL, json=json)
        return response.status_code, response.json()
    
    @allure.step('Создать заказ авторизированным пользователем')
    def post_create_order_with_token(self, accessToken, json):
        response = requests.post(CREATE_ORDER_URL, headers={"Authorization": accessToken}, json=json)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, response.text
    
    @allure.step('Получить заказ НЕ авторизированным пользователем')
    def get_order_no_token(self):
        response = requests.get(GET_ORDER_URL)
        return response.status_code, response.json()

    @allure.step('Получить заказ авторизированным пользователем')
    def get_order_with_token(self, accessToken):
        response = requests.get(GET_ORDER_URL, headers={"Authorization": accessToken})
        return response.status_code, response.json()

    @allure.step('Получить данные об ингредиентах')
    def get_ingredients(self):
        response = requests.get(GET_INGREDIENTS_URL)
        return response.status_code, response.json()
        