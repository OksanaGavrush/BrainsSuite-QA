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

## Running Tests
Use the following command to run tests:
```bash
pytest -v
