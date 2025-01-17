import pytest


def test_create_user_without_authorization_app(create_syns_user):
    create_syns_user.create_user_without_authorization()
    create_syns_user.check_status_code_is_400()
    create_syns_user.check_massage_authorization()


def test_no_duplicate_user_creation(create_syns_user, app_key):
    create_syns_user.no_create_user_already_exists(app_key)
    create_syns_user.validate_message_in_response()
    create_syns_user.check_status_code_is_200()


@pytest.mark.parametrize("gender", ["test", "123", "", [1, 2], 'MALE', 'Other'])
def test_invalid_gender(manager_syns_user, app_key, gender):
    manager_syns_user.check_invalid_gender(app_key, gender)
    manager_syns_user.check_status_code_is_400()


def test_validate_birth_year_in_future(manager_syns_user, app_key):
    manager_syns_user.validate_birth_year(app_key, 1899)
    manager_syns_user.check_status_code_is_400()


def test_missing_fields_in_request_body(manager_syns_user, app_key):
    manager_syns_user.request_missing_required_fields(app_key)
    manager_syns_user.check_status_code_is_400()


@pytest.mark.parametrize("birthdate", ["199-3-3", "", "1999-3-33", "1999-111-30", "wwww-05-05", "1000-e-31"])
def test_validate_birthdate(manager_syns_user, app_key, birthdate):
    manager_syns_user.valid_birthdate_check(app_key, birthdate)
    manager_syns_user.check_status_code_is_400()


def test_set_new_name_in_payload(manager_syns_user, token, app_key):
    manager_syns_user.update_payload_with_name(app_key)
    manager_syns_user.check_status_code_is_200()
    manager_syns_user.get_update_payload_with_name(token, app_key)
    manager_syns_user.check_status_code_is_200()


def test_put_updates_data(put_patient_info, token, app_key):
    put_patient_info.check_put_response(token, app_key)
    put_patient_info.check_status_code_is_200()


@pytest.mark.parametrize("name", [1, 1.24, [], {34: "1234567890"}])
def test_validate_name_with_invalid_input(put_patient_info, token, app_key, name):
    put_patient_info.check_validate_name_with_invalid_input(token, app_key, name)
    put_patient_info.check_status_code_is_400()


def test_patient_update_invalid_token(put_patient_info, token, app_key):
    put_patient_info.update_patient_with_invalid_token(token, app_key)
    put_patient_info.check_status_code_is_422()


def test_patient_update__without_token(put_patient_info, app_key):
    put_patient_info.update_patient_without_token(app_key)
    put_patient_info.check_status_code_is_401()


def test_patient_info_update(put_patient_info, token, app_key):
    put_patient_info.verify_patient_info_update(token, app_key)
    put_patient_info.check_status_code_is_200()


def test_get_patient_info_invalid_token(get_patient_info, token, app_key):
    get_patient_info.get_patient_info_invalid_token(token, app_key)
    get_patient_info.check_status_code_is_422()


def test_get_patient_info_invalid_parameter(get_patient_info, app_key):
    get_patient_info.get_patient_info_with_not_provided_token(app_key)
    get_patient_info.check_status_code_is_401()


def test_validate_json_schema(get_patient_info, token, app_key):
    get_patient_info.validate_json_schema(token, app_key)
    get_patient_info.check_status_code_is_200()


def test_get_patient_visits_invalid_parameter(get_patient_visits, token, app_key):
    get_patient_visits.get_patient_visits_invalid_token(token, app_key)
    get_patient_visits.check_status_code_is_422()


def test_get_patient_visits_without_token(get_patient_visits, app_key):
    get_patient_visits.get_patient_visits_with_not_provided_token(app_key)
    get_patient_visits.check_status_code_is_401()


def test_post_visits_with_invalid_token(post_patient_visits, token, app_key):
    post_patient_visits.create_visits_with_invalid_token(token, app_key)
    post_patient_visits.check_status_code_is_422()


def test_post_patient_visits_without_token(post_patient_visits, app_key):
    post_patient_visits.create_visits_without_token(app_key)
    post_patient_visits.check_status_code_is_401()


def test_get_patient_visit(get_patient_visits, token, app_key):
    get_patient_visits.get_patient_visits_valid_token(token, app_key)
    get_patient_visits.check_status_code_is_200()


def test_find_questionnaire_url(patient_questionnaire, token, app_key):
    patient_questionnaire.get_questionnaire_url(token, app_key)
    patient_questionnaire.check_status_code_is_200()


def test_complete_questionnaire(patient_questionnaire, token, app_key, driver):
    patient_questionnaire.get_questionnaire_url(token, app_key)
    patient_questionnaire.answer_survey_questions(driver)
    patient_questionnaire.get_url_with_patient_visits_id(token, app_key)
    patient_questionnaire.check_status_code_is_200()
    patient_questionnaire.verify_pdf_response(token, app_key)
    patient_questionnaire.check_status_code_is_200()


def test_questionnaire_info_update(patient_questionnaire, token, app_key, driver):
    patient_questionnaire.get_questionnaire_url(token, app_key)
    patient_questionnaire.check_status_code_is_200()
    patient_questionnaire.validate_empty_questionnaire_form(token, app_key)
    patient_questionnaire.check_status_code_is_200()
    patient_questionnaire.answer_survey_questions(driver)
    patient_questionnaire.get_url_with_patient_visits_id(token, app_key)


def test_extract_mri_uuid(patient_mri_upload, token, app_key):
    patient_mri_upload.get_patient_visits_id(token, app_key)
    patient_mri_upload.check_status_code_is_200()
    patient_mri_upload.patient_mri_upload_with_visits_id(token, app_key)
    patient_mri_upload.check_status_code_is_200()
    patient_mri_upload.patient_mri_upload_with_mri_uuid(token, app_key)
    patient_mri_upload.check_status_code_is_200()

