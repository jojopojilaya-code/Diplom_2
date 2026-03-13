import requests
import allure
from data import *
from helpers import *


class UserMethods:
    @allure.step('Создать пользователя')
    def post_create_user(self, params = None):
        if params is None:
            params = generate_user_data()
        response = requests.post(CREATE_USER_URL, json=params)  
        return response.status_code, response.json(), params   
      
    @allure.step('Авторизировать пользователя в системе')
    def post_login_user(self, json):
        response = requests.post(LOGIN_USER_URL, json=json)
        return response.status_code, response.json()  
      
    @allure.step('Удалить пользователя')
    def delete_user(self, accessToken, json):
        response = requests.delete(DELETE_USER_URL, headers={"Authorization": accessToken}, json=json)
        return response.status_code, response.json()  
    
    @allure.step('Обновить данные пользователя')
    def patch_change_user(self, accessToken, json):
        response = requests.patch(UPDATE_USER_DATA_URL, headers={"Authorization": accessToken}, json=json)
        return response.status_code, response.json()
