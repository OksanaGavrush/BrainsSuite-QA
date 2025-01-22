import requests
import allure

from endpoints.base_endpoint import BaseEndpoint
from endpoints.json_scheme import GetApiResponse


class GetPatientInfo(BaseEndpoint):
    @allure.step("Get patient info with invalid token")
    def get_patient_info_invalid_token(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token} + q",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    @allure.step("Get patient info without providing token")
    def get_patient_info_with_not_provided_token(self, app_key):
        headers = {
            "Authorization": '',
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    @allure.step("Validate JSON schema of patient info response")
    def validate_json_schema(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)
        self.response_data = GetApiResponse(**self.response.json())

    @allure.step("Update user information")
    def get_send_user_info_update(self, token, app_key, name, birthdate, gender):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)
        assert self.response.json()['data'].get('name') == name
        assert self.response.json()['data'].get('birthdate') == birthdate
        assert self.response.json()['data'].get('gender') == gender
