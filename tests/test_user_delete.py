import pytest
import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_delete_reserved_user(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user_id = self.get_json_value(response_login, 'user_id')

        Assertions.assert_status_code(response_login, 200)

        response_del = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response_del, 400)

        assert response_del.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response content: {response_del.content}"

        response_check = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}")

        Assertions.assert_status_code(response_check, 200)
        Assertions.assert_json_has_key(response_check, "username")

    def test_delete_just_created_user(self):
        # create_user
        data = self.prepare_registration_data()

        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, "id")

        user_id = self.get_json_value(response_create, "id")
        email = data["email"]
        password = data["password"]
        # login
        login_data = {
            'email': email,
            'password': password
        }

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')

        Assertions.assert_status_code(response_login, 200)
        # delete
        response_del = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response_del, 200)

        response_check = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}")

        print(response_check.status_code)
        print(response_check.content)

        Assertions.assert_status_code(response_check, 404)
        assert response_check.content.decode("utf-8") == f"User not found", f"Unexpected response content: {response_del.content}"

    def test_delete_auth_with_other_user(self):
        data1 = self.prepare_registration_data()

        response_create = requests.post("https://playground.learnqa.ru/api/user/", data=data1)

        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, "id")

        email = data1["email"]
        password = data1["password"]
        # login
        login_data = {
            'email': email,
            'password': password
        }

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        first_user_id = self.get_json_value(response_login, 'user_id')

        Assertions.assert_status_code(response_login, 200)

        data2 = self.prepare_registration_data()

        response_create2 = requests.post("https://playground.learnqa.ru/api/user/", data=data2)

        Assertions.assert_status_code(response_create, 200)
        Assertions.assert_json_has_key(response_create, "id")

        second_user_id = self.get_json_value(response_create, "id")

        response_del = requests.delete(
            f"https://playground.learnqa.ru/api/user/{second_user_id}",
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response_del, 400)

        response_check1 = requests.get(f"https://playground.learnqa.ru/api/user/{first_user_id}")

        Assertions.assert_status_code(response_check1, 200)
        Assertions.assert_json_has_key(response_check1, "username")

        response_check2 = requests.get(f"https://playground.learnqa.ru/api/user/{second_user_id}")

        Assertions.assert_status_code(response_check2, 200)
        Assertions.assert_json_has_key(response_check2, "username")



