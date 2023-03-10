from requests import Response
import json.decoder
from datetime import datetime

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie {cookie_name} in last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find cookie {header_name} in last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_json = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_json, f"Response JSON doesn't have key '{name}' "

        return response_as_json[name]

    def prepare_registration_data(self, email=None, username=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        if username is None:
            username = 'learnqa'
        return {
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
            'password': '1234'
        }