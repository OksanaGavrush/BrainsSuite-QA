# Project Overview
This project is dedicated to automating API and UI testing for BrainSuite, focusing on patient functionalities and MRI data uploads. We aim to cover both positive and negative scenarios comprehensively.

For testing, we utilize the [BrainSuite Public API](#).

## Technology Stack
- **Python**: For writing test scripts.
- **Pytest**: For organizing the tests and handling assertions.
- **Selenium**: For automating browser interactions.
- **Allure**: For generating detailed test reports.

## Setup
Tests are structured to demonstrate interaction with both API and UI. We manage test data and environment through `conftest.py`, where we also handle user authentication via token generation.

## Test Scenarios

### API Tests
1. **User Update Test**: This tests the update functionality where a POST request is made to update user details (`name`, `birthdate`, and `gender`), followed by a GET request to ensure the updates reflect correctly.
2. **Patient Visit Creation and Retrieval**:
   - POST request to create a patient visit.
   - GET request to retrieve the patient's questionnaire details.

### UI Tests with Selenium WebDriver
- **Survey Interaction Test**: Automates a web browser to handle survey responses, ensuring that the survey report is generated correctly as a PDF.

## Running Tests
Use the following command to run tests marked as "smoke":
```bash
pytest -m smoke
