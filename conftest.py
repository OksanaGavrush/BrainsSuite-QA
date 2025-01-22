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


@pytest.fixture(scope="session")
def app_key():
    with open('auth.txt', 'r') as file:
        return file.read().strip()


def get_headers(token, app_key):
    return {
        "Authorization": f"Bearer {token}",
        "Authorization-App": f"{app_key}",
    }


def get_token(app_key):
    if not os.path.exists('token.txt'):
        return request_new_token(app_key)

    with open('token.txt', 'r') as file:
        token = file.read().strip()

    validate_response = requests.get(
        'https://api.brainsuite.co.jp/patient/info',
        headers=get_headers(token, app_key)
    )
    if validate_response.status_code == 200:
        return token
    else:
        os.remove('token.txt')
        return request_new_token(app_key)


def request_new_token(app_key):
    headers = {
        "Authorization-App": f"{app_key}"
    }
    body = {
        "nlPatientId": "ALICEx1",
        "email": "doe690594+ALICEx1@gmail.com",
        "gender": "male",
        "birthdate": "1990-05-15",
        "name": "Alice Johnson"
    }
    response = requests.post('https://api.brainsuite.co.jp/nextlogic/sync', json=body, headers=headers)
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
def token(app_key):
    return get_token(app_key)


@pytest.fixture(scope="session")
def headers(token, app_key):
    return get_headers(token, app_key)


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
