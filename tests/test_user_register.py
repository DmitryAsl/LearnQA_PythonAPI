import pytest
import requests
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Register user")
class TestUserRegister(BaseCase):
    fields = [
        ({'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'email': "test@example.com", 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'password': '1234'}),
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': "test@example.com"})
    ]

    @allure.feature("create")
    @allure.tag("critical")
    @allure.description("This test check successfully create user")
    def test_create_user_successfull(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.feature("create")
    @allure.tag("critical")
    @allure.description("This test check not create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

    @allure.feature("create")
    @allure.tag("critical")
    @allure.description("This test check not create user with incorrect email")
    def test_create_user_with_incorrect_email(self):
        email = 'testexample.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @allure.feature("create")
    @allure.tag("critical")
    @allure.description("This test check not create user without some required fields")
    @pytest.mark.parametrize("data", fields)
    def test_create_user_without_required_field(self, data):
        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert "The following required params are missed:" in response.content.decode("utf-8"), f"Unexpected response content: {response.content}"

    @allure.feature("create")
    @allure.tag("major")
    @allure.description("This test check not create user with short username")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data(username='I')

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    @allure.feature("create")
    @allure.tag("critical")
    @allure.description("This test check not create user with longest username")
    def test_create_user_with_longest_username(self):
        username = '251_chapters_of_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_username_long_userna'
        data = self.prepare_registration_data(username=username)

        response = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long"
