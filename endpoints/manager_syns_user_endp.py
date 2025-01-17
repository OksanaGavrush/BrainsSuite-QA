import random
import requests
import allure

from endpoints.base_endpoint import BaseEndpoint


class ManagerSynsUser(BaseEndpoint):
    random_name = None

    @allure.step("Check invalid gender: {gender}")
    def check_invalid_gender(self, app_key, gender):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": gender,
            "birthdate": "1990-05-15"
        }
        with allure.step(f"Sending POST request with payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync',
                                          json=payload, headers=headers)

    @allure.step("Request with missing required fields")
    def request_missing_required_fields(self, app_key):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male"
        }
        with allure.step(f"Sending POST request with payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Check valid birthdate: {birthdate}")
    def valid_birthdate_check(self, app_key, birthdate):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male",
            "birthdate": birthdate,
        }
        with allure.step(f"Sending POST request with payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Validate birth year: {birthdate}")
    def validate_birth_year(self, app_key, birthdate):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male",
            "birthdate": birthdate,
        }
        with allure.step(f"Sending POST request with payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Update payload with random name")
    def update_payload_with_name(self, app_key):
        headers = {"Authorization-App": f"{app_key}"}
        names = ["Alice Johnson", "Bob Smith", "Charlie Williams", "Diana Brown"]
        self.random_name = f"{random.choice(names)}"
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male",
            "birthdate": "1990-05-15",
            "name": self.random_name,
        }
        with allure.step(f"Sending POST request with payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Get updated payload and validate name")
    def get_update_payload_with_name(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step("Sending GET request to fetch patient info"):
            self.response = requests.get('https://api.brainsuite.co.jp/patient/info', headers=headers)
        with allure.step("Parsing response JSON and validating name"):
            self.response_json = self.response.json()
            name = self.response_json.get("data", {}).get("name")
            assert self.random_name == name, "Name is not correct"

