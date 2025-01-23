import os
import pytest
import requests
from selenium import webdriver
from endpoints.post_nextlogic_sync_endpoint import PostSyncUser
from endpoints.put_patient_info import PutPatientInfo
from endpoints.get_patient_info import GetPatientInfo
from endpoints.get_patient_visits import GetPatientVisits
from endpoints.post_patient_visits import PostPatientVisits
from endpoints.patient_visits_questionnaire_check_link import PatientVisitsQuestionnaire
from endpoints.patient_mri_upload import PatientUpload
from selenium.webdriver.chrome.options import Options
from endpoints.base_endpoint import BaseEndpoint


@pytest.fixture(scope="session")
def base_endpoint():
    return BaseEndpoint()


def get_token(base_endpoint):
    if not os.path.exists('token.txt'):
        return request_new_token(base_endpoint)

    with open('token.txt', 'r') as file:
        token = file.read().strip()

    headers = get_headers(token, base_endpoint)
    validate_response = requests.get(f'{base_endpoint.base_url}/patient/info', headers=headers)
    if validate_response.status_code == 200:
        return token
    else:
        os.remove('token.txt')
        return request_new_token(base_endpoint)


def get_headers(token, base_endpoint):
    return {
        "Authorization": f"Bearer {token}",
        "Authorization-App": base_endpoint.auth_app
    }


def request_new_token(base_endpoint):
    headers = {
        "Authorization-App": f"{base_endpoint.auth_app}"
    }
    body = {
        "nlPatientId": "ALICEx1",
        "email": "doe690594+ALICEx1@gmail.com",
        "gender": "male",
        "birthdate": "1990-05-15",
        "name": "Alice Johnson"
    }
    response = requests.post(f'{base_endpoint.base_url}/nextlogic/sync', json=body, headers=headers)
    if response.status_code == 200:
        token = response.json().get('data', {}).get('token')
        if not token:
            raise Exception("Token not found in response")
        with open('token.txt', 'w') as file:
            file.write(token)
        return token
    else:
        raise Exception(f"Failed to retrieve new token: {response.status_code}, {response.text}")


@pytest.fixture(scope="session")
def token(base_endpoint):
    return get_token(base_endpoint)


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def post_syns_user():
    return PostSyncUser()


@pytest.fixture
def put_patient_info():
    return PutPatientInfo()


@pytest.fixture
def get_patient_info():
    return GetPatientInfo()


@pytest.fixture
def get_patient_visits():
    return GetPatientVisits()


@pytest.fixture
def post_patient_visits():
    return PostPatientVisits()


@pytest.fixture
def patient_questionnaire():
    return PatientVisitsQuestionnaire()


@pytest.fixture
def patient_mri_upload():
    return PatientUpload()
