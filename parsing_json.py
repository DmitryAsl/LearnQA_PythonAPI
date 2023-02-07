import json
from json.decoder import JSONDecodeError

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
try:
    text_to_json = json.loads(json_text)
    second_message = text_to_json['messages'][1]['message']
    print(second_message)
except JSONDecodeError:
    print("Variable 'json_text' is not a JSON import ")