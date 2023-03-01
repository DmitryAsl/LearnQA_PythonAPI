import pytest
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import  allure

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("user/login", data=data)
        #response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, 'auth_sid')
        self.token = self.get_header(response1, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(response1, 'user_id')

    @allure.description("This test successfully authorize user")
    def test_auth_user(self):

        response2 = MyRequests.get(
            "user/auth",
            cookies = {"auth_sid": self.auth_sid},
            headers = {"x-csrf-token": self.token}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            f"User_id from auth method is not equal user_id from check method {response2.json()['user_id']}, {self.user_id_from_auth_method}"
        )

    @allure.description("This test checks authorization status w-o sending auth cookie or header")
    @pytest.mark.parametrize("conditions", exclude_params)
    def test_negative_auth_check(self, conditions):
        if conditions == "no_cookies":
            response2 = MyRequests.get(
                "user/auth",
                headers={"token": self.token}
            )
        else:
            response2 = MyRequests.get(
                "user/auth",
                cookies = {"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with conditions {conditions}"
        )

