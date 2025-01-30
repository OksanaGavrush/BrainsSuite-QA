import pytest


@pytest.mark.smoke
def test_create_user_without_authorization_app(post_syns_user):
    post_syns_user.create_user_without_authorization()
    post_syns_user.check_status_code_is_400()
    post_syns_user.check_massage_authorization()


@pytest.mark.smoke
def test_no_duplicate_user_creation(post_syns_user):
    post_syns_user.no_create_user_already_exists()
    post_syns_user.validate_message_in_response()
    post_syns_user.check_status_code_is_200()


@pytest.mark.smoke
def test_send_name_success(post_syns_user, get_patient_info, token,):
    post_syns_user.send_user_info_update("Alice", "1990-07-15", "male")
    post_syns_user.check_status_code_is_200()
    get_patient_info.send_user_info_update(token, "Alice", "1990-07-15", "male")
    get_patient_info.check_status_code_is_200()


@pytest.mark.smoke
def test_gender_missing(post_syns_user):
    post_syns_user.sending_request_without_gender()
    post_syns_user.check_status_code_is_400()


@pytest.mark.smoke
@pytest.mark.parametrize("gender", ["female", "male", "other"])
def test_gender_female_or_male_or_other(post_syns_user, gender):
    post_syns_user.gender_acceptance_validator(gender)
    post_syns_user.check_status_code_is_200()


@pytest.mark.smoke
@pytest.mark.parametrize("gender", ["test", "123", "", [1, 2], 'MALE', 'Other'])
def test_invalid_gender(post_syns_user, gender):
    post_syns_user.check_invalid_gender(gender)
    post_syns_user.check_status_code_is_400()


@pytest.mark.smoke
def test_validate_birth_year_in_future(post_syns_user):
    post_syns_user.validate_birth_year(1899)
    post_syns_user.check_status_code_is_400()


@pytest.mark.smoke
def test_missing_birthdate(post_syns_user):
    post_syns_user.request_missing_birthdate()
    post_syns_user.check_status_code_is_400()


@pytest.mark.smoke
@pytest.mark.parametrize("birthdate", ["199-3-3", "", "1999-3-33", "1999-111-30", "wwww-05-05", "1000-e-31"])
def test_validate_birthdate(post_syns_user, birthdate):
    post_syns_user.valid_birthdate_check(birthdate)
    post_syns_user.check_status_code_is_400()


@pytest.mark.smoke
def test_validate_put_response(put_patient_info, token):
    put_patient_info.validate_put_response(token)
    put_patient_info.check_status_code_is_200()


@pytest.mark.smoke
def test_patient_update_invalid_token(put_patient_info, token):
    put_patient_info.update_patient_with_invalid_token(token)
    put_patient_info.check_status_code_is_422()


@pytest.mark.smoke
def test_patient_update_without_token(put_patient_info):
    put_patient_info.update_patient_without_token()
    put_patient_info.check_status_code_is_401()


@pytest.mark.smoke
def test_patient_info_update(put_patient_info, get_patient_info, token):
    put_patient_info.verify_patient_info_update(token, "Alice LI", "male", "1991-11-25")
    put_patient_info.check_status_code_is_200()
    get_patient_info.send_user_info_update(token, "Alice LI", "1991-11-25", "male")


@pytest.mark.smoke
@pytest.mark.parametrize("name", [1, 1.24, [], {34: "1234567890"}])
def test_validate_name_with_invalid_input(put_patient_info, token, name):
    put_patient_info.validate_name_with_invalid_input_name(token, name)
    put_patient_info.check_status_code_is_400()


@pytest.mark.smoke
@pytest.mark.parametrize("gender", ["female", "male", "other"])
def test_gender_validation(put_patient_info, token, gender):
    put_patient_info.gender_acceptance_validator(token, gender)
    put_patient_info.check_status_code_is_200()


@pytest.mark.smoke
def test_get_patient_info_invalid_token(get_patient_info, token):
    get_patient_info.get_patient_info_invalid_token(token)
    get_patient_info.check_status_code_is_422()


@pytest.mark.smoke
def test_get_patient_info_invalid_parameter(get_patient_info):
    get_patient_info.get_patient_info_with_not_provided_token()
    get_patient_info.check_status_code_is_401()


@pytest.mark.smoke
def test_validate_json_schema(get_patient_info, token):
    get_patient_info.validate_json_schema(token)
    get_patient_info.check_status_code_is_200()


@pytest.mark.smoke
def test_get_patient_visits_invalid_parameter(get_patient_visits, token):
    get_patient_visits.get_patient_visits_invalid_token(token)
    get_patient_visits.check_status_code_is_422()


@pytest.mark.smoke
def test_get_patient_visits_without_token(get_patient_visits):
    get_patient_visits.get_patient_visits_with_not_provided_token()
    get_patient_visits.check_status_code_is_401()


@pytest.mark.smoke
def test_post_visits_with_invalid_token(post_patient_visits, token):
    post_patient_visits.create_visits_with_invalid_token(token)
    post_patient_visits.check_status_code_is_422()


@pytest.mark.smoke
def test_post_patient_visits_without_token(post_patient_visits):
    post_patient_visits.create_visits_without_token()
    post_patient_visits.check_status_code_is_401()


@pytest.mark.smoke
def test_get_patient_visit(get_patient_visits, token):
    get_patient_visits.get_patient_visits_valid_token(token)
    get_patient_visits.check_status_code_is_200()


@pytest.mark.regression
def test_complete_questionnaire(patient_questionnaire, token, driver):
    patient_questionnaire.get_questionnaire_url_and_visits_id(token)
    patient_questionnaire.validate_empty_questionnaire_form(token)
    patient_questionnaire.answer_survey_questions_page(driver)
    patient_questionnaire.update_patient_info_and_check_completed_questionnaire(token)
    patient_questionnaire.check_status_code_is_200()
    patient_questionnaire.get_url_b_and_verify_pdf_response(token)
    patient_questionnaire.check_status_code_is_200()


@pytest.mark.regression
def test_upload_mri_files_to_patient_mri_and_upload_pdf(patient_mri_upload, token):
    patient_mri_upload.unzip_mri_data()
    patient_mri_upload.create_patient_visits_and_get_visits_id(token)
    patient_mri_upload.check_status_code_is_200()
    patient_mri_upload.post_payload_patient(token)
    patient_mri_upload.get_mri_uuid()
    patient_mri_upload.check_status_code_is_200()
    patient_mri_upload.upload_files_with_mri_uuid(token)
    patient_mri_upload.check_status_code_is_200()
    patient_mri_upload.get_report_url_upload_files(token)
    patient_mri_upload.verify_pdf_response(token)

