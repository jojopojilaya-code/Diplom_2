import pytest
from methods.user_methods import UserMethods
from methods.order_methods import OrderMethods

@pytest.fixture
def create_user():
    """
    Фикстура создаёт нового пользователя и возвращает его данные 
    (status_code, response_data, user_data).
    После завершения теста пользователь удаляется.
    """
    user_methods = UserMethods()
    status_code, response_data,  payload = user_methods.post_create_user()  
    user_data = {
        "email": response_data["user"]["email"],
        "password": payload["password"],
        "name": response_data["user"]["name"],
        "accessToken": response_data["accessToken"],
        "refreshToken": response_data["refreshToken"]
    }
    yield status_code, response_data, user_data
    user_methods.delete_user(
        accessToken = user_data["accessToken"], 
        json = {"email": user_data["email"], "password": user_data["password"]}
    )


@pytest.fixture
def authorization_user(create_user):
    """
    Фикстура авторизует пользователя и возвращает его данные:
    (status_code, login_response, user_data)
    """
    _, _, user_data = create_user
    payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    _, login_response = UserMethods().post_login_user(json=payload)
    
    user_data.update({
        "accessToken": login_response["accessToken"],
        "refreshToken": login_response["refreshToken"]
    })
    yield user_data

@pytest.fixture()
def ingredients():
    """Фикстура возвращает список ингредиентов или None если не удалось получить"""
    status_code, response = OrderMethods().get_ingredients()
    return response.get("data") if status_code == 200 else None
