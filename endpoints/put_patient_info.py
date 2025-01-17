import requests
from endpoints.base_endpoint import BaseEndpoint

PAYLOAD = {
    "name": "Alice Johnson",
    "gender": "male",
    "birthdate": "1990-05-15"
}


class PutPatientInfo(BaseEndpoint):

    def check_put_response(self, token, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)
        