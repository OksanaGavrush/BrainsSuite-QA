import random

import requests
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from endpoints.base_endpoint import BaseEndpoint


class PatientVisitsQuestionnaire(BaseEndpoint):

    @allure.step("Get questionnaire URL and visit ID")
    def get_questionnaire_url_and_visits_id(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.post(f'{self.base_url}/patient/visits', headers=headers)
        self.questionnaire_url = self.response.json()["data"].get('questionnaire')[0].get('url')
        self.visit_id = self.response.json()["data"]['visitId']
        print(self.questionnaire_url)

    @allure.step("Validate that questionnaire form is empty")
    def validate_empty_questionnaire_form(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }

        self.response = requests.get(f'{self.base_url}/patient/visits/{self.visit_id}', headers=headers)
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
    def answer_survey_questions_page(self, driver):
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
        questions = [
            ("walk_every_day", 'input[name="66"] + .oshn__radio-btn'),
            ("week_exercise", 'input[name="67"] + .oshn__radio-btn'),
            ("daily_fruit_veggie_bowls", 'input[name="68"] + .oshn__radio-btn'),
            ("weekly_seafood_fillets", 'input[name="69"] + .oshn__radio-btn'),
            ("sleep_quality_last_month", 'input[name="70"] + .oshn__radio-btn'),
            ("selected_sleep_factors", 'label[class="ocmc"]'),
            ("hypertension_status", 'input[name="72"] + .oshn__radio-btn'),
            ("has_diabetes", 'input[name="73"] + .oshn__radio-btn'),
            ("smoking_status", 'input[name="74"] + .oshn__radio-btn'),
            ("daily_alcohol_intake", 'input[name="75"] + .oshn__radio-btn')
        ]
        for name, selector in questions:
            wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, selector)))
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            random.choice(elements).click()
            self.driver.execute_script("window.scrollBy(0, 300);")
        wait.until(ec.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".page-question__progress-bar span"), "66%"))
        next_button = wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="進む ▶︎"]')))
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click().perform()
        questions = [
            ("felt_nervous_last_30_days", 'input[name="76"] + .oshs__radio-btn'),
            ("felt_hopeless_last_30_days", 'input[name="77"] + .oshs__radio-btn'),
            ("felt_restless_last_30_days", 'input[name="78"] + .oshs__radio-btn'),
            ("felt_downhearted_last_30_days", 'input[name="79"] + .oshs__radio-btn'),
            ("felt_exhausted_last_30_days", 'input[name="80"] + .oshs__radio-btn'),
            ("felt_worthless_last_30_days", 'input[name="81"] + .oshs__radio-btn')
        ]
        for name, selector in questions:
            wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, selector)))
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            random.choice(elements).click()
            self.driver.execute_script("window.scrollBy(0, 300);")
        wait.until(ec.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".page-question__progress-bar span"), "100%"))
        next_button = wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="進む ▶︎"]')))
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click().perform()

    @allure.step("Update patient info and check completed questionnaire")
    def update_patient_info_and_check_completed_questionnaire(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        with allure.step(f"Sending GET request to retrieve report URL"):
            self.response = requests.get(f'{self.base_url}/patient/visits/'
                                         f'{self.visit_id}', headers=headers)

        score_keys = [
            'BMIScore', 'exerciseScore', 'dietScore',
            'sleepScore', 'comorbiditiesScore',
            'smokeScore', 'alcoholScore', 'stressScore'
        ]

        for key in score_keys:
            value = self.response.json()['data']['questionnaire'][0].get(key, {}).get('score')
            assert isinstance(value, str), f"{key} score is not a string. Got: {type(value)}"

    @allure.step("Verify that the report is a valid PDF")
    def get_url_b_and_verify_pdf_response(self, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Authorization-App": f"{self.auth_app}",
        }
        self.response = requests.get(f'{self.base_url}/patient/visits/'
                                     f'{self.visit_id}', headers=headers)
        get_report_url_b = self.response.json()['data']['report']['B'].get('url')
        pdf_response = requests.get(get_report_url_b, headers=headers)
        assert pdf_response.headers['Content-Type'] == 'application/pdf'
