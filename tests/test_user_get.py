import pytest
import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        unexpected_fields = ['email', 'firstName', 'lastName']
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_keys(response, unexpected_fields)

    def test_get_user_details_auth_as_some_user(self):
        expected_fields = ['username', 'email', 'firstName', 'lastName']
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
            cookies = {"auth_sid": auth_sid},
            headers = {"x-csrf-token": token}
        )

        Assertions.assert_json_has_keys(response2, expected_fields)
