# OrangeHRM QA Automation & Quality Assurance Suite

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-WebDriver_4.48-green.svg)](https://www.selenium.dev/)
[![PyTest](https://img.shields.io/badge/PyTest-Framework-orange.svg)](https://pytest.org/)
[![Design Pattern](https://img.shields.io/badge/Design%20Pattern-Page%20Object%20Model%20(POM)-purple.svg)]()
[![Status](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)]()

This repository contains the complete solution for the **QA Engineer Assignment 2026**, covering:
1. **Manual Testing Suite:** Comprehensive test cases for **Login** (12 cases) and **PIM Employee Management** (View, Update, Delete).
2. **Defect Analysis:** 3 potential bugs and usability defects with reproduction steps, severity, and remediation strategies.
3. **Automated Test Suite:** A robust, enterprise-grade Python + Selenium test framework following the **Page Object Model (POM)**.
4. **End-to-End Workflow:** Automated Login -> Mouse hover over PIM -> Batch addition of 4 employees -> Viewport smooth scroll verification with `"Name Verified"` printed -> Dashboard logout.
5. **Reporting & Artifacts:** Excel spreadsheet (`TEST_CASES_ORANGEHRM.xlsx`), CSV (`TEST_CASES_LOGIN_AND_PIM.csv`), PyTest HTML report (`reports/test_report.html`), and a 2–3 minute Loom video script (`LOOM_WALKTHROUGH_SCRIPT.md`).

---

## 📁 Repository Structure

```
omnify/
├── config/
│   ├── __init__.py
│   └── config.py               # Centralized configuration, URLs, credentials & timeouts
├── pages/
│   ├── __init__.py
│   ├── base_page.py            # Base Page with explicit waits, hover, scroll & screenshots
│   ├── login_page.py           # Login Page Object & Locators
│   ├── dashboard_page.py       # Dashboard Page Object (topbar, PIM hover, logout)
│   └── pim_page.py             # PIM Module Page Object (Add, List, Scroll, Verify, Delete)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # PyTest fixtures, browser drivers, failure screenshots
│   ├── test_login.py           # 6 automated PyTest test cases for login
│   └── test_pim_workflow.py    # E2E assignment workflow test
├── reports/
│   ├── screenshots/            # Failure screenshots
│   └── test_report.html        # Interactive PyTest HTML report
├── .gitignore                  # Git ignore rules
├── generate_excel_report.py    # Script to build styled Excel workbook
├── LOOM_WALKTHROUGH_SCRIPT.md  # 2-3 minute presentation video script with cues
├── pytest.ini                  # PyTest runner settings
├── QA_ASSIGNMENT_REPORT.md     # Detailed QA submission document
├── requirements.txt            # Python dependencies
├── run_automation.py           # Standalone one-command workflow runner
├── TEST_CASES_LOGIN_AND_PIM.csv# Portable CSV test case dataset
└── TEST_CASES_ORANGEHRM.xlsx   # Formatted multi-tab Excel test suite
```

---

## ⚙️ Prerequisites & Setup

### 1. Requirements
- **Python 3.10+** (Tested with Python 3.12.10)
- **Google Chrome** (v120+) or **Microsoft Edge**
- **Git** installed

### 2. Installation
Clone the repository and install all required dependencies:
```bash
git clone <your-repo-url>
cd omnify
pip install -r requirements.txt
```

---

## 🚀 Running the Automation

### Method 1: Standalone Runner Script (Recommended)
Run the full 5-step workflow end-to-end:
```bash
# Headless Mode (Fast, background execution):
python run_automation.py

# Headed Mode (Visible browser window):
python run_automation.py --headed
```

**Expected Console Output:**
```
================================================================================
  ORANGEHRM AUTOMATION WORKFLOW - PAGE OBJECT MODEL (POM)
  Browser: Headless=True | Target URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
================================================================================

[STEP 1/5] Automating Login Flow...
SUCCESS: Logged in successfully as 'Admin'.

[STEP 2/5] Navigating to PIM Module (Mouse Hover & Click)...
SUCCESS: Hovered over PIM menu item and navigated to PIM Module.

[STEP 3/5] Adding 3-4 Employees in PIM Module...
   -> Creating Employee 1/4: Alice8103 Johnson...
      Saved: Alice8103 Johnson (Employee ID: 0563)
   -> Creating Employee 2/4: Bob8103 Smith...
      Saved: Bob8103 Smith (Employee ID: 0564)
   -> Creating Employee 3/4: Carol8103 Williams...
      Saved: Carol8103 Williams (Employee ID: 0565)
   -> Creating Employee 4/4: David8103 Brown...
      Saved: David8103 Brown (Employee ID: 0566)
SUCCESS: Total 4 employees added to OrangeHRM.

[STEP 4/5] Verifying Employees in Employee List...
   -> Checking Employee: Alice8103 Johnson (ID: 0563)...
[VERIFICATION SUCCESS] Located Employee: Alice8103 Johnson (ID: 0563)
Name Verified
   -> Checking Employee: Bob8103 Smith (ID: 0564)...
[VERIFICATION SUCCESS] Located Employee: Bob8103 Smith (ID: 0564)
Name Verified
   -> Checking Employee: Carol8103 Williams (ID: 0565)...
[VERIFICATION SUCCESS] Located Employee: Carol8103 Williams (ID: 0565)
Name Verified
   -> Checking Employee: David8103 Brown (ID: 0566)...
[VERIFICATION SUCCESS] Located Employee: David8103 Brown (ID: 0566)
Name Verified
SUCCESS: All added employees located with smooth scrolling and names verified.

[STEP 5/5] Logging Out from the Dashboard...
SUCCESS: Logged out cleanly. Returned to Login Page.

================================================================================
  ALL 5 WORKFLOW STEPS EXECUTED AND PASSED SUCCESSFULLY!
================================================================================
```

### Method 2: Running via PyTest
Execute test suites with automated reporting:
```bash
# Run all tests (Login + PIM Workflow)
pytest

# Run only Login test suite
pytest tests/test_login.py

# Run only PIM workflow test
pytest tests/test_pim_workflow.py
```
After execution, open `reports/test_report.html` in your browser to inspect test logs and metrics.

### Method 3: Rebuilding Excel Workbook
To regenerate the formatted Excel report:
```bash
python generate_excel_report.py
```

---

## 📋 Summary of Manual Test Cases

| Test Case ID | Module | Scenario / Objective | Status |
| :--- | :--- | :--- | :---: |
| **TC_LOG_001** | Login | Verify login with valid credentials (`Admin` / `admin123`) | **PASS** |
| **TC_LOG_002** | Login | Verify login attempt with invalid password | **PASS** |
| **TC_LOG_003** | Login | Verify login attempt with non-existent username | **PASS** |
| **TC_LOG_004** | Login | Verify validation when submitting blank credentials | **PASS** |
| **TC_LOG_005** | Login | Verify validation when Username is provided but Password is blank | **PASS** |
| **TC_LOG_006** | Login | Verify validation when Password is provided but Username is blank | **PASS** |
| **TC_LOG_007** | Login | Verify Password field masking (`type="password"`) | **PASS** |
| **TC_LOG_008** | Login | Verify Password case-sensitivity handling | **PASS** |
| **TC_LOG_009** | Login | Verify SQL Injection resilience in input fields | **PASS** |
| **TC_LOG_010** | Login | Verify navigation to Forgot Password page | **PASS** |
| **TC_LOG_011** | Login | Verify session termination and Back button handling upon Logout | **PASS** |
| **TC_LOG_012** | Login | Verify route guard prevents direct unauthenticated dashboard access | **PASS** |
| **TC_PIM_001** | PIM | Verify navigation to PIM module via sidebar hover and click | **PASS** |
| **TC_PIM_002** | PIM | Verify adding single employee with mandatory fields | **PASS** |
| **TC_PIM_003** | PIM | Verify batch addition of 4 unique employees | **PASS** |
| **TC_PIM_004** | PIM | Verify locating newly added employee in Employee List | **PASS** |
| **TC_PIM_005** | PIM | Verify smooth table scrolling and DOM card location | **PASS** |
| **TC_PIM_006** | PIM | Verify updating employee personal details | **PASS** |
| **TC_PIM_007** | PIM | Verify deleting an employee with modal confirmation | **PASS** |
| **TC_PIM_008** | PIM | Verify cancelling employee deletion preserves record | **PASS** |

*For complete step-by-step descriptions and test data, see [QA_ASSIGNMENT_REPORT.md](QA_ASSIGNMENT_REPORT.md) or [TEST_CASES_ORANGEHRM.xlsx](TEST_CASES_ORANGEHRM.xlsx).*

---

## 🐛 Identified Defects & Usability Issues

1. **`BUG-001` (High Severity): Exposure of Plaintext Administrative Credentials on Public Login Page**
   - Credentials `Admin` / `admin123` are printed in plaintext inside the public DOM container.
2. **`BUG-002` (High Severity): Lack of Rate Limiting or Account Lockout (Brute Force Risk)**
   - Unlimited consecutive failed login attempts are accepted without CAPTCHA challenges, exponential backoff, or temporary account lockouts.
3. **`BUG-003` (Medium Severity): Missing Password Visibility Toggle & Low-Contrast Focus States**
   - Password input lacks an eye icon toggle to reveal characters, and the submit button focus ring violates WCAG 2.1 Level AA accessibility standards.

---

## 🎥 Loom Video Walkthrough

A structured 2–3 minute video script with timestamps and exact talking points is available in [LOOM_WALKTHROUGH_SCRIPT.md](LOOM_WALKTHROUGH_SCRIPT.md).

---

## 📤 Pushing to GitHub

To push this codebase to your own GitHub repository for submission:
```bash
git init
git add .
git commit -m "feat: complete OrangeHRM QA manual test suite and POM automation framework"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
