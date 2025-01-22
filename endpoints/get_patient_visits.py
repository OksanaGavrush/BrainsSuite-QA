import requests
import allure

from endpoints.base_endpoint import BaseEndpoint


class GetPatientVisits(BaseEndpoint):
    get_url_b = None

    @allure.step("Get patient visits with invalid token")
    def get_patient_visits_invalid_token(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token} + q",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    @allure.step("Get patient visits without providing token")
    def get_patient_visits_with_not_provided_token(self, app_key):
        headers = {
            "Authorization": '',
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)

    @allure.step("Get patient visits with valid token")
    def get_patient_visits_valid_token(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.get('https://api.brainsuite.co.jp/patient/visits', headers=headers)
