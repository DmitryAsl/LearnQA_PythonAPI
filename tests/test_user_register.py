import pytest
import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random

class TestUserRegister(BaseCase):
    fields = [
        ({'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com"})
    ]

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfull(self):
        data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            'password': '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
            'password': '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"

    def test_create_user_with_incorrect_email(self):
        email = 'testexample.com'
        data = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
            'password': '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @pytest.mark.parametrize("data", fields)
    def test_create_user_without_required_field(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert "The following required params are missed:" in response.content.decode("utf-8"), f"Unexpected response content: {response.content}"

    def test_create_user_with_short_username(self):
        data = {
            'username': 'I',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            'password': '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    def test_create_user_with_longest_usertname(self):
        username = '251_chapters_of_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_userna'
        data = {
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email,
            'password': '1234'
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long"
