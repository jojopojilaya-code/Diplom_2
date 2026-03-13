import pytest
from methods.user_methods import UserMethods
from methods.order_methods import OrderMethods
from helpers import generate_user_data


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def create_user():
    user_methods = UserMethods()

    payload = generate_user_data()
    status_code, response_data, _ = user_methods.post_create_user(payload)

    user_data = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": response_data.get("accessToken"),
        "refreshToken": response_data.get("refreshToken")
    }

    yield status_code, response_data, user_data

    if user_data["accessToken"]:
        user_methods.delete_user(
            accessToken=user_data["accessToken"],
            json={
                "email": user_data["email"],
                "password": user_data["password"]
            }
        )


@pytest.fixture
def authorization_user(create_user):
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
    status_code, response = OrderMethods().get_ingredients()
    return response.get("data") if status_code == 200 else None
