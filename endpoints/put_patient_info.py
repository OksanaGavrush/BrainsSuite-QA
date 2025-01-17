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

    @allure.step("Check PUT response with payload: {payload}")
    def check_put_response(self, token, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending PUT request to update patient info with headers: {headers}"):
            self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)

    @allure.step("Validate name with invalid input: {name}")
    def check_validate_name_with_invalid_input(self, token, app_key, name):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        payload = {
            "name": name,
            "gender": "male",
            "birthdate": "1999-01-05"
        }
        with allure.step(f"Sending PUT request with invalid name: {payload}"):
            self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)

    @allure.step("Update patient with invalid token")
    def update_patient_with_invalid_token(self, token, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token} + a",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending PUT request without token. Headers: {headers}"):
            self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)

    @allure.step("Update patient without token")
    def update_patient_without_token(self, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending PUT request without token. Headers: {headers}"):
            self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)

    @allure.step("Verify patient info update")
    def verify_patient_info_update(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        payload = {
            "name": "Jon Johnson",
            "gender": "other",
            "birthdate": "1991-05-15"
        }
        with allure.step(f"Sending PUT request to update patient info. Payload: {payload}"):
            self.response = requests.put('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)
        with allure.step("Validating PUT response status code"):
            assert self.response.status_code == 200, f"Expected 200, got {self.response.status_code}"

        with allure.step("Sending GET request to verify patient info update"):
            self.get_response = requests.get('https://api.brainsuite.co.jp/patient/info', json=payload, headers=headers)
        updated_data = self.get_response.json().get("data", {})

        with allure.step("Validating updated data"):
            allure.attach(str(updated_data), name="Updated Patient Info", attachment_type=allure.attachment_type.JSON)
            assert updated_data.get("name") == payload["name"], \
                f"Expected name '{payload['name']}', but got '{updated_data.get('name')}'"
            assert updated_data.get("gender") == payload["gender"], \
                f"Expected gender '{payload['gender']}', but got '{updated_data.get('gender')}'"
            assert updated_data.get("birthdate") == payload["birthdate"], \
                f"Expected birthdate '{payload['birthdate']}', but got '{updated_data.get('birthdate')}'"
