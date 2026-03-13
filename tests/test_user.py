import pytest
import allure
from data import *
from helpers import *
from methods.user_methods import UserMethods


class TestUserCreate:

    @allure.title(
        '''Позитивный сценарий создания пользователя: передаем все обязательные поля (email, password, name).'''
    )
    @allure.description('ОР: Пользователь успешно создан.')
    def test_create_user_email_password_name_created_successfully(self, create_user):
        status_code, response_data, _ = create_user

        assert status_code == 200
        assert response_data["success"] is True
        assert "user" in response_data
        assert "accessToken" in response_data


    @allure.title('Негативный сценарий создания пользователя: email уже есть в системе.')
    @allure.description('ОР: Пользователь не создан, запрос возвращает ошибку.')
    def test_create_user_already_exists_error(self, create_user):
        _, _, existing_user = create_user
        params = {
            "email": existing_user["email"],
            "password": existing_user["password"],
            "name": existing_user["name"]
        }
        status_code, response_data, _ = UserMethods().post_create_user(params)
        assert all([
            status_code == 403,
            response_data["success"] is False,
            response_data["message"] == USER_EXISTS
        ]), (
            f"Ошибка проверки существующего пользователя.\n"
            f"Статус: {status_code} (ожидалось 403).\n"
            f"Success: {response_data.get('success')} (ожидалось False).\n"
            f"Сообщение: '{response_data.get('message')}'\n"
            f"(ожидалось '{USER_EXISTS}').\n\n"
            f"Полный ответ: {response_data}\n"
        )


    @allure.title('Негативный сценарий: создание пользователя без обязательного поля')
    @allure.description('ОР: Пользователь не создан, запрос возвращает ошибку.')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_missing_required_field(self, missing_field):
        user_data = generate_user_data()
        user_data.pop(missing_field)
        status_code, response_data, _ = UserMethods().post_create_user(params=user_data)
        assert all([
            status_code == 403,
            response_data["success"] is False,
            response_data["message"] == REQUIRED_FIELDS
        ]), (
            f"Ошибка при пропуске поля '{missing_field}'.\n"
            f"Статус: {status_code} (ожидалось 403).\n"
            f"Success: {response_data.get('success')} (ожидалось False).\n"
            f"Сообщение: '{response_data.get('message')}'\n"
            f"(ожидалось '{REQUIRED_FIELDS}').\n\n"
            f"Отправленные данные: {user_data}\n"
        )


class TestUserLogin:

    @allure.title('Позитивный сценарий: успешная авторизация существующего пользователя')
    @allure.description('ОР: Пользователь успешно авторизован, возвращаются accessToken и refreshToken')
    def test_login_existing_user_success(self, create_user):
        _, _, user_data = create_user
        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json=params)
        assert all([
            status_code == 200,
            response_data["success"] is True,
            "accessToken" in response_data,
            "refreshToken" in response_data,
            response_data["user"]["email"] == user_data["email"],
            response_data["user"]["name"] == user_data["name"]
        ]), (
            f"Ошибка авторизации пользователя.\n"
            f"Статус: {status_code} (ожидалось 200).\n"
            f"Success: {response_data.get('success')} (ожидалось True).\n"
            f"Наличие токена: {'accessToken' in response_data} (ожидалось True).\n"
            f"Email:     {response_data.get('user', {}).get('email')}\n"
            f"(ожидалось {user_data['email']}).\n\n"
            f"Полный ответ: {response_data}\n"
        )


    @allure.title('Негативный сценарий: авторизация с неверным паролем')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_login_wrong_password_error(self, create_user):
        _, _, user_data = create_user
        params = {
            "email": user_data["email"],
            "password": "invalid_pass_" + user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json=params)
        assert all([
            status_code == 401,
            response_data["success"] is False,
            response_data["message"] == LOGIN_ERROR
        ]), (
            f"Ошибка проверки неверного пароля.\n" 
            f"Статус: {status_code} (ожидалось 401).\n"
            f"Сообщение: '{response_data.get('message')}'\n"
            f"(ожидалось '{LOGIN_ERROR}').\n\n"
            f"Ответ сервера: {response_data}\n"
        )


    @allure.title('Негативный сценарий: авторизация с несуществующим email')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_login_non_existing_email_error(self):
        user_data = generate_user_data()     
        params = {
            "email": "nvalid_email_" + user_data["email"],
            "password": user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json=params)
        assert all([
            status_code == 401,
            response_data["success"] is False,
            response_data["message"] == LOGIN_ERROR
        ]), (
            f"Ошибка проверки несуществующего email.\n"
            f"Статус: {status_code} (ожидалось 401).\n"
            f"Сообщение: '{response_data.get('message')}'\n"
            f"(ожидалось '{LOGIN_ERROR}').\n\n"
            f"Ответ сервера: {response_data}\n"
        )


    @allure.title('Негативный сценарий: авторизация без обязательного поля')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized при отсутствии обязательных полей')
    @pytest.mark.parametrize('missing_field', ['email', 'password'])
    def test_login_missing_required_field(self, missing_field):
        user_data = generate_user_data()
        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        params.pop(missing_field)
        status_code, response_data = UserMethods().post_login_user(json=params)
        assert all([
            status_code == 401,
            response_data["success"] is False,
            response_data["message"] == LOGIN_ERROR
        ]), (
            f"Ошибка при пропуске поля {missing_field}.\n"
            f"Статус: {status_code} (ожидалось 401).\n"
            f"Сообщение: '{response_data.get('message')}\n"
            f"(ожидалось '{LOGIN_ERROR}').\n\n"
            f"Ответ сервера: {response_data}\n"
        )


class TestUserUpdate:

    @allure.title('Позитивный сценарий: изменение данных пользователя с авторизацией')
    @allure.description('ОР: Данные пользователя успешно изменены, возвращается обновленная информация')
    def test_update_user_data_success(self, authorization_user):
        user_data = authorization_user            
        new_data = generate_user_data()
        update_data = {
            "email": new_data["email"],
            "name": new_data["name"]
        }
        status_code, response_data = UserMethods().patch_change_user(
            accessToken=user_data["accessToken"],
            json=update_data
        )
        assert all([
            status_code == 200,
            response_data["success"] is True,
            response_data["user"]["email"] == update_data["email"],
            response_data["user"]["name"] == update_data["name"]
        ]), (
            f"Ошибка обновления данных.\n"
            f"Статус: {status_code} (ожидалось 200).\n\n"
            f"Ответ сервера: {response_data}\n"
        )


    @allure.title('Негативный сценарий: изменение данных без авторизации')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_update_user_data_unauthorized(self, create_user):
        _, _, user_data = create_user
        update_data = {
            "email": user_data["email"],
            "name": user_data["name"]
        }
        status_code, response_data = UserMethods().patch_change_user(
            accessToken="invalid_token",
            json=update_data
        )
        assert all([
            status_code == 401,
            response_data["success"] is False,
            response_data["message"] == AUTH_REQUIRED
        ]), (
            f"Ошибка проверки авторизации.\n"
            f"Статус: {status_code} (ожидалось 401).\n"
            f"Сообщение: '{response_data.get('message')}'\n"
            f"(ожидалось '{AUTH_REQUIRED}').\n\n"
            f"Ответ сервера: {response_data}\n"
        )
