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


class PostSyncUser(BaseEndpoint):

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

    @allure.step("Check user info update")
    def send_user_info_update(self, app_key, name, birthdate, gender):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": gender,
            "birthdate": birthdate,
            "name": name
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Check send request without gender")
    def sending_request_without_gender(self, app_key):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "birthdate": "1990-05-15",
            "name": "Jon"
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)
        assert 'Invalid data' in self.response.json()['msg'], ("Expected 'Invalid data'"
                                                               " message is missing in the API response")

    @allure.step("Validate gender acceptance with gender: {gender}")
    def gender_acceptance_validator(self, app_key, gender):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": gender,
            "birthdate": "1990-04-15"
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

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
    def request_missing_birthdate(self, app_key):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male"
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Check valid birthdate: {birthdate}")
    def valid_birthdate_check(self, app_key, birthdate):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male",
            "birthdate": birthdate,
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)

    @allure.step("Validate birth year: {birthdate}")
    def validate_birth_year(self, app_key, birthdate):
        headers = {"Authorization-App": f"{app_key}"}
        payload = {
            "nlPatientId": "ALICEx1",
            "gender": "male",
            "birthdate": birthdate,
        }
        self.response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=payload, headers=headers)


