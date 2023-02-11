import requests

# part 1
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

# part 2
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method':'POST'})
print(response.text)
print(response.status_code)

# part 3
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method':'POST'})
print(response.text)
print(response.status_code)

#part 4
methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']

for method in methods:
    response_get = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': method})
    print(f"HTTP-метод {response_get.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_get.text}'; Статус код ответа {response_get.status_code} ")
    response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_post.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_post.text}'; Статус код ответа {response_post.status_code} ")
    response_put = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_put.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_put.text}'; Статус код ответа {response_put.status_code} ")
    response_delete = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_delete.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_delete.text}'; Статус код ответа {response_delete.status_code} ")
    response_patch = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_patch.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_patch.text}'; Статус код ответа {response_patch.status_code} ")
    response_head = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_head.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_head.text}'; Статус код ответа {response_head.status_code} ")
    response_options = requests.options("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method': method})
    print(f"HTTP-метод {response_options.request.method}; Передаваемый параметр method {method}; Текст ответа на запрос '{response_options.text}'; Статус код ответа {response_options.status_code} ")