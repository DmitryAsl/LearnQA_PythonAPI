import pytest
from lib.BaseCase import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # register
        data = self.prepare_registration_data()

        response1 = MyRequests.post("user/", data=data)

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

        response2 = MyRequests.post("user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        Assertions.assert_status_code(response2, 200)
        #edit
        new_name = 'Changed FirstName'

        response3 = MyRequests.put(
            f"user/{user_id}",
            data={'firstName': new_name},
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response3, 200)

        response4 = MyRequests.get(
            f"user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            f"Value of firstName is incorrect after edit"
        )

    def test_edit_some_user_no_auth(self):
        user_id = 63453
        response1 = MyRequests.get(f"user/{user_id}")

        Assertions.assert_status_code(response1, 200)

        username = self.get_json_value(response1, "username")
        new_username = "New_learnqa"
        response2 = MyRequests.put(
            f"user/{user_id}",
            data={'username': new_username}
        )

        Assertions.assert_status_code(response2, 400)

        response3 = MyRequests.get(f"user/{user_id}")
        username_new = self.get_json_value(response3, "username")

        Assertions.assert_status_code(response3, 200)
        Assertions.assert_json_value_by_name(response3, "username", username,
                                             f"Username was changed. This is the fail")

    def test_edit_some_user_auth_another_user(self):
        data = {
            'email': 'dmitry_test@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("user/login", data=data)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response_login, 'user_id')

        response_get = MyRequests.get(
            f"user/{user_id_from_auth_method}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )
        username_auth_user = self.get_json_value(response_get, "username")

        user_id_other_user = 63453
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_username = f"New_learnqa_{random_part}"

        response_get_user = MyRequests.get(f"user/{user_id_other_user}")
        username_old = self.get_json_value(response_get_user, "username")

        response_put = MyRequests.put(
            f"user/{user_id_other_user}",
            data={'username': new_username},
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token}
        )

        Assertions.assert_status_code(response_put, 422)

        response_get_other_user = MyRequests.get(f"user/{user_id_other_user}")
        response_get_auth_user = MyRequests.get(f"user/{user_id_from_auth_method}")

        Assertions.assert_json_value_by_name(response_get_other_user, "username", username_old,
                                             f"Username was changed. This is fail")
        Assertions.assert_json_value_by_name(response_get_auth_user, "username", username_auth_user,
                                             f"Username was changed. This is fail")

    def test_edit_auth_user_with_incorrect_email(self):
        # register
        data = self.prepare_registration_data()

        response1 = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = data["email"]
        password = data["password"]
        # login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        Assertions.assert_status_code(response2, 200)
        # edit
        new_email = 'test_example.com'

        response3 = MyRequests.put(
            f"user/{user_id}",
            data={'email': new_email},
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content: {response3.content}"

    def test_edit_auth_user_with_short_firstName(self):
        # register
        data = self.prepare_registration_data()

        response1 = MyRequests.post("user/", data=data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = data["email"]
        password = data["password"]
        # login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        Assertions.assert_status_code(response2, 200)
        # edit
        new_firstName = 'I'

        response3 = MyRequests.put(
            f"user/{user_id}",
            data={'firstName': new_firstName},
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_status_code(response3, 400)
        assert f"Too short value for field firstName" in response3.content.decode("utf-8"), f"Unexpected response content: {response3.content}"
