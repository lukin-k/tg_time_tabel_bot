import requests
import json

class Bot:
    def __init__(self, token):
        self.token=token
        self.api_url='https://api.telegram.org/bot'+token+'/'

    def get_updates(self, offset=None, timeout=30):
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url+'getUpdates', data=params)
        return response.json()['result']

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            return get_result[-1]
        else:
            return 0
        
    def send_message(self, chat_id, text):  
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.api_url + 'sendMessage', data=params)
        return response
