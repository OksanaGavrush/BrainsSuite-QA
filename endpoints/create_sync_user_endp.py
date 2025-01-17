import requests
import allure

from endpoints.base_endpoint import BaseEndpoint
from endpoints.json_scheme import ApiResponse

PAYLOAD = {
    "nlPatientId": "ALICEx1",
    "email": "doe690594+ALICEx1@gmail.com",
    "gender": "male",
    "birthdate": "1990-05-15",
    "name": "Alice Johnson"
}


class CreateSyncUser(BaseEndpoint):

    @allure.step("Create user without authorization")
    def create_user_without_authorization(self, payload=None):
        payload = payload if payload else PAYLOAD
        with allure.step(f"Payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload)
        with allure.step("Parsing response JSON"):
            self.response_json = self.response.json()

    @allure.step("Check message for missing authorization")
    def check_massage_authorization(self):
        expected_message = "Wrong or inactive Authorization-App header"
        actual_message = self.response_json.get("msg")
        assert actual_message == expected_message, f"Expected message: '{expected_message}', got: '{actual_message}'"

    @allure.step("Attempt to create user that already exists")
    def no_create_user_already_exists(self, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {"Authorization-App": f"{app_key}"}
        with allure.step(f"Sending POST request with headers: {headers} and payload: {payload}"):
            self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)
        with allure.step("Parsing response into ApiResponse object"):
            self.response_data = ApiResponse(**self.response.json())
        with allure.step("Validating response data"):
            self.response_data.data.nlPatientId = 'ALICEx1'

    @allure.step("Validate success message in response")
    def validate_message_in_response(self):
        expected_message = 'Successfully synced.'
        actual_message = self.response_data.msg
        assert actual_message == expected_message, \
            f"Validation Error: Expected message '{expected_message}', got: '{actual_message}'"


