import shutil
import time
import zipfile
from pathlib import Path

import requests
import allure

from endpoints.base_endpoint import BaseEndpoint
from mri_upload_utils import send_files_in_batches, gather_hashes_from_directory

BASE_DIR = Path(__file__).resolve().parent.parent
MRI_DATA_PATH = BASE_DIR / "mri_data"


class PatientUpload(BaseEndpoint):
    @allure.step("Unzipping MRI data files")
    def unzip_mri_data(self):
        zip_path = BASE_DIR / "mri_data.zip"
        extract_path = BASE_DIR / "mri_data"
        if extract_path.exists():
            shutil.rmtree(extract_path)
        extract_path.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"File {zip_path} has been extracted to {extract_path}")

    @allure.step("Get patient visits")
    def create_patient_visits_and_get_visits_id(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.post(f'{self.base_url}/patient/visits', headers=headers)
        self.visit_id = self.response.json()["data"]['visitId']

    @allure.step("Initializing MRI upload for visit")
    def post_payload_patient(self, token):
        payload = {
            "file_hashes":  gather_hashes_from_directory(MRI_DATA_PATH),
            "out_hospital_id": "ALICEx3",
            "out_hospital_name": "Central Medical Hospital",
            "out_hospital_prefecture": "Tokyo",
            "out_hospital_address": "123 Health St., Tokyo, Japan",
            "out_hospital_phone_number": "+81 123-456-7890",
            "out_hospital_email": "doe690594+ALICEx3@gmail.com"
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.post(f'{self.base_url}/patient/mri/upload/init/{self.visit_id}',
                                      headers=headers, json=payload)

    @allure.step("Retrieve MRI UUID from response")
    def get_mri_uuid(self):
        self.mri_uuid = self.response.json()['data'].get('mriUuid')

    @allure.step("Uploading MRI data from")
    def upload_files_with_mri_uuid(self, token, folder_path=None):
        folder_path = MRI_DATA_PATH
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        url = f'{self.base_url}/patient/mri/upload/{self.mri_uuid}'
        responses = send_files_in_batches(folder_path, url, headers)
        for response in responses:
            assert response.json()['msgCode'] == 'S002'
            assert response.json()['data'].get('status')

    def get_report_url_upload_files(self, token, timeout=60, interval=5):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.response = requests.get(f'{self.base_url}/patient/visits/{self.visit_id}',
                                         headers=headers)
            try:
                self.report_url_a = self.response.json()['data']["report"].get('A').get('url')
                if self.report_url_a:
                    return self.report_url_a
            except (KeyError, AttributeError, TypeError) as e:
                print(f"Error in response structure: {e}")
            time.sleep(interval)
        raise TimeoutError("Report URL did not appear within the specified time.")

    @allure.step("Verify that the report is a valid PDF")
    def verify_pdf_response(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        with allure.step(f"Sending GET request to validate PDF"):
            pdf_response = requests.get(self.report_url_a, headers=headers)
            assert pdf_response.headers['Content-Type'] == 'application/pdf'
