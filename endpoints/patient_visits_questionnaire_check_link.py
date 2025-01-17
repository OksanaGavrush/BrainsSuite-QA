import random
import requests
from time import sleep

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from endpoints.base_endpoint import BaseEndpoint


class PatientVisitsQuestionnaire(BaseEndpoint):
    questionnaire_url = None
    get_url_b = None
    pdf_response = None
    driver = None

    @allure.step("Get questionnaire URL and visit ID")
    def get_questionnaire_url(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending POST request to retrieve questionnaire URL with headers: {headers}"):
            self.response = requests.post('https://api.brainsuite.co.jp/patient/visits', headers=headers)
        self.questionnaire_url = self.response.json()["data"].get('questionnaire')[0].get('url')
        self.visit_id = self.response.json()["data"]['visitId']

    @allure.step("Validate that questionnaire form is empty")
    def validate_empty_questionnaire_form(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step("Sending GET request to retrieve questionnaire data"):
            self.response = requests.get(f'https://api.brainsuite.co.jp/patient/visits/{self.visit_id}', headers=headers)
            response_json = self.response.json()

        score_keys = [
            'BMIScore', 'exerciseScore', 'dietScore',
            'sleepScore', 'comorbiditiesScore',
            'smokeScore', 'alcoholScore', 'stressScore'
        ]
        with allure.step("Validating that all score fields are empty"):
            for key in score_keys:
                assert response_json['data']['questionnaire'][0].get(key, {}).get('score') is None, \
                    f"{key} score is not None"

    @allure.step("Answer survey questions")
    def answer_survey_questions(self, driver):
        self.driver = driver
        self.driver.get(self.questionnaire_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(ec.presence_of_element_located((By.XPATH, '//input[@type="number"][1]')))
        actions = ActionChains(self.driver)
        send_height = self.driver.find_element(By.XPATH, '//input[@type="number"][1]')
        (actions.click(send_height).send_keys(Keys.BACKSPACE).send_keys(Keys.BACKSPACE)
         .send_keys(Keys.BACKSPACE).send_keys('170').perform())
        send_weight = self.driver.find_element(By.XPATH, '//*[@id="root"]/main/div[3]/div/div/div')
        actions.click(send_weight).send_keys(Keys.BACKSPACE).send_keys(Keys.BACKSPACE).send_keys('65').perform()
        walk_every_day = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="66"] + .oshn__radio-btn')
        random.choice(walk_every_day).click()
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[name="67"] + .oshn__radio-btn')))
        week_exercise = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="67"] + .oshn__radio-btn')
        random.choice(week_exercise).click()
        self.driver.execute_script("window.scrollBy(0, 600);")
        daily_fruit_veggie_bowls = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="68"] + .oshn__radio-btn')
        random.choice(daily_fruit_veggie_bowls).click()
        weekly_seafood_fillets = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="69"] + .oshn__radio-btn')
        random.choice(weekly_seafood_fillets).click()
        self.driver.execute_script("window.scrollBy(0, 500);")
        sleep_quality_last_month = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="70"] + .oshn__radio-btn')
        random.choice(sleep_quality_last_month).click()
        selected_sleep_factors = self.driver.find_elements(By.CSS_SELECTOR, 'label[class="ocmc"]')
        random.choice(selected_sleep_factors).click()
        self.driver.execute_script("window.scrollBy(0, 700);")
        hypertension_status = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="72"] + .oshn__radio-btn')
        random.choice(hypertension_status).click()
        has_diabetes = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="73"] + .oshn__radio-btn')
        random.choice(has_diabetes).click()
        smoking_status = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="74"] + .oshn__radio-btn')
        random.choice(smoking_status).click()
        self.driver.execute_script("window.scrollBy(0, 500);")
        daily_alcohol_intake = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="75"] + .oshn__radio-btn')
        random.choice(daily_alcohol_intake).click()
        sleep(2)
        next_button = self.driver.find_element(By.XPATH, '//button[text()="進む ▶︎"]')
        next_button.click()
        sleep(2)
        felt_nervous_last_30_days = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="76"] + .oshs__radio-btn')
        random.choice(felt_nervous_last_30_days).click()
        felt_hopeless_last_30_days = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="77"] + .oshs__radio-btn')
        random.choice(felt_hopeless_last_30_days).click()
        felt_restless_last_30_days = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="78"] + .oshs__radio-btn')
        random.choice(felt_restless_last_30_days).click()
        self.driver.execute_script("window.scrollBy(0, 800);")
        felt_downhearted_last_30_days = (self.driver.find_elements
                                         (By.CSS_SELECTOR, 'input[name="79"] + .oshs__radio-btn'))
        random.choice(felt_downhearted_last_30_days).click()
        felt_exhausted_last_30_days = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="80"] + .oshs__radio-btn')
        random.choice(felt_exhausted_last_30_days).click()
        felt_worthless_last_30_days = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="81"] + .oshs__radio-btn')
        random.choice(felt_worthless_last_30_days).click()
        sleep(2)
        self.driver.find_element(By.XPATH, '//button[text()="進む ▶︎"]').click()
        sleep(1)

    @allure.step("Get patient visit with ID")
    def get_patient_visits_with_id(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending GET request to retrieve report URL for visit ID: {self.visit_id}"):
            self.response = requests.get(f'https://api.brainsuite.co.jp/patient/visits/'
                                         f'{self.visit_id}', headers=headers)

    @allure.step("Get URL with patient visit ID")
    def get_url_with_patient_visits_id(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending GET request to retrieve report URL for visit ID: {self.visit_id}"):
            self.response = requests.get(f'https://api.brainsuite.co.jp/patient/visits/'
                                         f'{self.visit_id}', headers=headers)
        response_json = self.response.json()

        score_keys = [
            'BMIScore', 'exerciseScore', 'dietScore',
            'sleepScore', 'comorbiditiesScore',
            'smokeScore', 'alcoholScore', 'stressScore'
        ]

        for key in score_keys:
            value = response_json['data']['questionnaire'][0].get(key, {}).get('score')
            assert isinstance(value, str), f"{key} score is not a string. Got: {type(value)}"

    @allure.step("Verify that the report is a valid PDF")
    def verify_pdf_response(self, token, app_key):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{app_key}",
        }
        with allure.step(f"Sending GET request to validate PDF at: {self.get_url_b}"):
            pdf_response = requests.get(f'{self.get_url_b}', headers=headers)
        assert pdf_response.headers['Content-Type'] == 'application/pdf'
