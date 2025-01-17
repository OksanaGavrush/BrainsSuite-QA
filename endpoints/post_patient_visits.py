import allure
import requests

from endpoints.base_endpoint import BaseEndpoint


class PostPatientVisits(BaseEndpoint):

    @allure.step("Create visits with invalid token")
    def create_visits_with_invalid_token(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token} + a",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending POST request with invalid token. Headers: {headers}"):
            self.response = requests.post('https://api.brainsuite.co.jp/patient/visits', headers=headers)

    @allure.step("Create visits without token")
    def create_visits_without_token(self, app_key):
        headers = {
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending POST request without token. Headers: {headers}"):
            self.response = requests.post('https://api.brainsuite.co.jp/patient/visits', headers=headers)
