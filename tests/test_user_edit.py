import pytest
import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # register
        data = self.prepare_registration_data()

        response1 = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = data["email"]
        password = data["password"]
        #login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        Assertions.assert_status_code(response2, 200)
        #edit
        new_name = 'Changed FirstName'

        response3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            data={'firstName': new_name},
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response3, 200)

        response4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            f"Value of firstName is incorrect after edit"
        )


