import pytest
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserGet(BaseCase):
    unexpected_fields = ['email', 'firstName', 'lastName']
    expected_fields = ['username', 'email', 'firstName', 'lastName']
    data = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("user/2")

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_keys(response, self.unexpected_fields)

    def test_get_user_details_auth_as_some_user(self):
        response1 = MyRequests.post("user/login", data=self.data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(
            f"user/{user_id_from_auth_method}",
            cookies = {"auth_sid": auth_sid},
            headers = {"x-csrf-token": token}
        )

        Assertions.assert_json_has_keys(response2, self.expected_fields)

    def test_get_user_details_auth_as_other_user(self):

        response1 = MyRequests.post("user/login", data=self.data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')

        response2 = MyRequests.get(
            f"huser/1",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_no_keys(response2, self.unexpected_fields)
