import allure
import requests

from endpoints.base_endpoint import BaseEndpoint


class PostPatientVisits(BaseEndpoint):

    @allure.step("Create visits with invalid token")
    def create_visits_with_invalid_token(self, token):
        headers = {
            "Authorization": f"Bearer {token} + a",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.post(f'{self.base_url}/patient/visits', headers=headers)

    @allure.step("Create visits without token")
    def create_visits_without_token(self):
        headers = {
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.post(f'{self.base_url}/patient/visits', headers=headers)
