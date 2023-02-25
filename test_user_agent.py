import requests
import pytest

class TestUserAgent():
    test_data = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1', {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0', {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

    @pytest.mark.parametrize('User_agent, exp_value', test_data)
    def test_user_agent(self, User_agent, exp_value):
        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'
        data = {'User-agent': User_agent}
        expected_value = exp_value

        response = requests.get(url, headers=data)
        assert response.status_code == 200, "Wrong status code"
        response_as_dict = response.json()
        assert 'platform' in response_as_dict, "There is no platform in response"
        assert 'browser' in response_as_dict, "There is no browser in response"
        assert 'device' in response_as_dict, "There is no device in response"

        assert expected_value['platform'] == response_as_dict['platform'], f"The platform value is incorrect"
        assert expected_value['browser'] == response_as_dict['browser'], f"The browser value is incorrect"
        assert expected_value['device'] == response_as_dict['device'], f"The device value is incorrect"



