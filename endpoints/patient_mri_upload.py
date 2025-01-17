import requests
import allure
from pathlib import Path

from endpoints.base_endpoint import BaseEndpoint
from mri_upload_utils import send_files_in_batches, gzip_file, send_files, gather_hashes_from_directory


BASE_DIR = Path(__file__).resolve().parent.parent
directory_path = BASE_DIR / "mri_data"

file_hashes = gather_hashes_from_directory(directory_path)

PAYLOAD = {
  "file_hashes": file_hashes,
  "out_hospital_id": "ALICEx1",
  "out_hospital_name": "Central Medical Hospital",
  "out_hospital_prefecture": "Tokyo",
  "out_hospital_address": "123 Health St., Tokyo, Japan",
  "out_hospital_phone_number": "+81 123-456-7890",
  "out_hospital_email": "doe690594+ALICEx1@gmail.com"
}


class PatientUpload(BaseEndpoint):
    mri_uuid = None

    @allure.step("Get patient visits")
    def get_patient_visits_id(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.post('https://api.brainsuite.co.jp/patient/visits', headers=headers)
        self.visit_id = self.response.json()["data"]['visitId']

    @allure.step("Initializing MRI upload for visit")
    def patient_mri_upload_with_visits_id(self, token, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.post(f'https://api.brainsuite.co.jp/patient/mri/upload/init/{self.visit_id}',
                                      headers=headers, json=payload)
        self.mri_uuid = self.response.json()['data'].get('mriUuid')

    @allure.step("Uploading MRI data from")
    def patient_mri_upload_with_mri_uuid(self, token, app_key, folder_path=None):
        folder_path = directory_path
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        url = f'https://api.brainsuite.co.jp/patient/mri/upload/{self.mri_uuid}'
        responses = send_files_in_batches(folder_path, url, headers)
        for response in responses:
            assert response.json()['msgCode'] == 'S002'
            assert response.json()['data'].get('status')
