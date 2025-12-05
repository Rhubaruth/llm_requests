import requests
from time import time


def send_prompt(prompt, token):
    payload = {
        'model': 'gpt-oss-120b',
        'messages': [
            # {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ]
    }

    try:
        # NLP server
        start_time = time()
        result: requests.Response = requests.post(
            "https://nlp.fi.muni.cz/llama/v1/chat/completions",
            headers={'Authorization': f'Bearer {token}'},
            json=payload
        )
        end_time = time()

    except requests.exceptions.ReadTimeout:
        result_dict = {
            'content': '',
            'duration': end_time - start_time,
            'status': -1
        }
        return result_dict

    if result.status_code != 200:
        result_dict = {
            'content': result,
            'duration': end_time - start_time,
            'status': result.status_code
        }
        return result_dict
    result_json = result.json()['choices'][0]
    if 'message' in result_json:
        message = result_json['message']['content']
        result_dict = {
            'content': message,
            'duration': end_time - start_time,
            'status': result.status_code
        }
        return result_dict
