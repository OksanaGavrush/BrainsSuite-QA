import requests
import allure

from endpoints.base_endpoint import BaseEndpoint
from endpoints.json_scheme import GetApiResponse


class GetPatientInfo(BaseEndpoint):
    @allure.step("Get patient info with invalid token")
    def get_patient_info_invalid_token(self, token):
        headers = {
            "Authorization": f"Bearer {token} + q",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.get(f'{self.base_url}/patient/info', headers=headers)

    @allure.step("Get patient info without providing token")
    def get_patient_info_with_not_provided_token(self):
        headers = {
            "Authorization": '',
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.get(f'{self.base_url}/patient/info', headers=headers)

    @allure.step("Validate JSON schema of patient info response")
    def validate_json_schema(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.get(f'{self.base_url}/patient/info', headers=headers)
        self.response_data = GetApiResponse(**self.response.json())

    @allure.step("Update user information")
    def send_user_info_update(self, token, name, birthdate, gender):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.get(f'{self.base_url}/patient/info', headers=headers)
        assert self.response.json()['data'].get('name') == name, "The returned name does not match the expected name."
        assert self.response.json()['data'].get(
            'birthdate') == birthdate, "The returned birthdate does not match the expected birthdate."
        assert self.response.json()['data'].get(
            'gender') == gender, "The returned gender does not match the expected gender."
