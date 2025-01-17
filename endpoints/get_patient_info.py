import requests
from endpoints.base_endpoint import BaseEndpoint
from endpoints.json_scheme import GetApiResponse


class GetPatientInfo(BaseEndpoint):

    def get_patient_info_invalid_token(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token} + q",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    def get_patient_info_with_not_provided_token(self, token, app_key):
        headers = {
            "Authorization": '',
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    def validate_json_schema(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)
        self.response_data = GetApiResponse(**self.response.json())