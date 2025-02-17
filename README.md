# BrainSuite QA Automation Project

## Project Overview
This project is dedicated to automating API and UI testing for BrainSuite, focusing on patient functionalities and MRI data uploads. We aim to cover both positive and negative scenarios comprehensively.
- **Purpose**: Automate testing to ensure the reliability and efficiency of patient-related features and MRI data handling within BrainSuite.
- **Tools Used**: Utilizes the BrainSuite Public API for comprehensive testing.

## Technology Stack
The selection of technologies is designed to provide a robust framework for writing, organizing, and running automated tests.
- **Python**: Used for writing test scripts due to its versatility and support for testing frameworks.
- **Pytest**: Chosen for its ability to handle complex test suites and its powerful assertion tools.
- **Selenium**: Utilized for its capabilities in automating browser interactions, essential for UI testing.
- **Allure**: Employed for generating detailed and visually informative test reports.

## Setup
Describes the initial setup process, focusing on how tests are structured and managed within the project environment.
- **Configuration**: Demonstrates interaction with both API and UI components.
- **Environment Management**: Explains the management of test data and authentication via `conftest.py`.

## Running Tests
Provides instructions on how to execute the tests, detailing the necessary commands and any relevant flags.
- **Command to Run Tests**: To execute the tests, use the following command in your terminal:
  ```bash
  pytest -v

