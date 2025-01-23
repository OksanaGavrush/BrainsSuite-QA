import requests
import allure

from endpoints.base_endpoint import BaseEndpoint

PAYLOAD = {
    "name": "Alice Johnson",
    "gender": "male",
    "birthdate": "1990-05-15"
}


class PutPatientInfo(BaseEndpoint):
    get_response = None

    @allure.step("Check PUT response with payload")
    def validate_put_response(self, token, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        with allure.step(f"Sending PUT request to update patient"):
            self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)

    @allure.step("Update patient with invalid token")
    def update_patient_with_invalid_token(self, token, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token} + a",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)

    @allure.step("Update patient without token")
    def update_patient_without_token(self, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)

    @allure.step("Verify patient info update")
    def verify_patient_info_update(self, token, name, gender, birthdate):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        payload = {
            "name": name,
            "gender": gender,
            "birthdate": birthdate
        }

        self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)

    @allure.step("Validate name with invalid input name")
    def validate_name_with_invalid_input_name(self, token, name):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        payload = {
            "name": name,
            "gender": "male",
            "birthdate": "1999-01-05"
        }
        self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)

    @allure.step("Validate gender acceptance with gender")
    def gender_acceptance_validator(self, token, gender):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        payload = {
            "name": "ALICE",
            "gender": gender,
            "birthdate": "1990-04-15"
        }
        self.response = requests.put(f'{self.base_url}/patient/info', json=payload, headers=headers)