import allure


class BaseEndpoint:
    response = None
    status_code = None
    response_json = None
    response_data = None
    visit_id = None

    @allure.step("Check status code is 400")
    def check_status_code_is_400(self):
        assert self.response.status_code == 400, f"Expected 400, got {self.response.status_code}"

    @allure.step("Check status code is 200")
    def check_status_code_is_200(self):
        assert self.response.status_code == 200, f"Expected 200, got {self.response.status_code}"

    @allure.step("Check status code is 202")
    def check_status_code_is_202(self):
        assert self.response.status_code == 202, f"Expected 202, got {self.response.status_code}"

    @allure.step("Check status code is 422")
    def check_status_code_is_422(self):
        assert self.response.status_code == 422, f"Expected 422, got {self.response.status_code}"

    @allure.step("Check status code is 401")
    def check_status_code_is_401(self):
        assert self.response.status_code == 401, f"Expected 401, got {self.response.status_code}"
