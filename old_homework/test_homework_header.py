import requests

class TestHomeworkHeader:
    def test_check_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        headers = response.headers
        print(headers)
        assert "x-secret-homework-header" in headers, f"These is no 'x-secret-homework-header' header in the response"

        value = headers.get("x-secret-homework-header")
        assert value == "Some secret value", f"The header 'x-secret-homework-header' value is incorrect"
