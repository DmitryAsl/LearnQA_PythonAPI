import requests

class TestHomeworkCookie:
    def test_check_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        coockies = response.cookies
        print(coockies)
        assert "HomeWork" in coockies, f"These is no 'HomeWork' cookie in the response"

        value = coockies.get("HomeWork")
        assert value == "hw_value", f"The coockie 'Homework' value is incorrect"
