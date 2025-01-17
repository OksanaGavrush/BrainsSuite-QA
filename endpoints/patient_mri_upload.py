import os

import requests
import allure
import hashlib
import json
import gzip

from endpoints.base_endpoint import BaseEndpoint

directory_path = "/Users/oksana/qa/Brainsuite_api_testing/mri_data"


def get_md5_hash(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        return hashlib.md5(data).hexdigest()


def gather_hashes_from_directory(directory_path):
    return [get_md5_hash(os.path.join(directory_path, f)) for f in os.listdir(directory_path) if
            os.path.isfile(os.path.join(directory_path, f))]


json_str = gather_hashes_from_directory(directory_path)
file_hashes = json.dumps(json_str)

PAYLOAD = {
  "file_hashes": f'{file_hashes}',
  "out_hospital_id": "ALICEx1",
  "out_hospital_name": "Central Medical Hospital",
  "out_hospital_prefecture": "Tokyo",
  "out_hospital_address": "123 Health St., Tokyo, Japan",
  "out_hospital_phone_number": "+81 123-456-7890",
  "out_hospital_email": "doe690594+ALICEx1@gmail.com"
}


class PatientPopulate(BaseEndpoint):
    mri_uuid = None

    @allure.step("Get patient visits")
    def get_patient_visits_id(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.post('https://api.brainsuite.co.jp/patient/visits', headers=headers)
        self.visit_id = self.response.json()["data"]['visitId']

    def patient_mri_upload_with_visits_id(self, token, app_key, payload=None):
        payload = payload if payload else PAYLOAD
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        self.response = requests.post(f'https://api.brainsuite.co.jp/patient/mri/upload/init/{self.visit_id}',
                                      headers=headers, json=payload)
        self.mri_uuid = self.response.json()['data'].get('mriUuid')
        import pdb;
        pdb.set_trace()





