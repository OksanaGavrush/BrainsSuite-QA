import requests
from endpoints.base_endpoint import BaseEndpoint

PAYLOAD = {
    "nlPatientId": "ALICEx1",
    "email": "doe690594+ALICEx1@gmail.com",
    "gender": "male",
    "birthdate": "1990-05-15",
    "name": "Alice Johnson"
}


class CreateSyncUser(BaseEndpoint):
    response = None
    status_code = None

    def create_user_without_authorization(self, payload=None):
        payload = payload if payload else PAYLOAD
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload)
        self.status_code = self.response.status_code

    def check_massage_authorization(self):
        assert self.response.json().get("msg") == "Wrong or inactive Authorization-App header"
