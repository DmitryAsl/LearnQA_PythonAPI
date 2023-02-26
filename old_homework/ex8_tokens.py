import requests
import json
import time

create_task = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
response = json.loads(create_task.text)

token = response['token']
seconds = response['seconds']

check_task = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
check_task_json = json.loads(check_task.text)
status = check_task_json['status']

if status == "Job is NOT ready":
    time.sleep(seconds)
    check_task = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={'token': token})
    check_task_json = json.loads(check_task.text)
    status = check_task_json['status']
    if status == "Job is ready":
        result = check_task_json['result']
        print(f"status task - {status}; result - {result}")
    else:
        print(f"status Uncorrect - {status}")
else:
    print(f"status Uncorrect - {status}")

