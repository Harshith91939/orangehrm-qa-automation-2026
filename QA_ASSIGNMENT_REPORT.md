# QA Engineer Assignment 2026: Comprehensive Evaluation & Automation Report

**Candidate Role:** QA Automation Engineer  
**Target Application:** OrangeHRM Open Source Demo (`https://opensource-demo.orangehrmlive.com/web/index.php/auth/login`)  
**Test Environment:** Windows 11 | Python 3.12.10 | Selenium WebDriver 4.48.0 | PyTest 9.1.1 | Google Chrome 122+  
**Deliverables Produced:**
1. Manual Test Suite for Login Functionality (12 Test Cases, exceeding the required 8)
2. Manual Test Suite & Scenarios for Employee Management (View, Update, Delete)
3. 3 In-Depth Bug and Usability Defect Reports (Security, Rate Limiting, Accessibility)
4. Full Page Object Model (POM) Automation Test Suite (Python + Selenium + PyTest)
5. Structured Excel Workbook (`TEST_CASES_ORANGEHRM.xlsx`) and CSV (`TEST_CASES_LOGIN_AND_PIM.csv`)
6. 2-3 Minute Loom Video Walkthrough Script (`LOOM_WALKTHROUGH_SCRIPT.md`)

---

## 1. Executive Summary

This report documents the quality assurance evaluation of the **OrangeHRM** web application. Testing encompassed both comprehensive manual test design and an industry-standard test automation framework implemented with **Python**, **Selenium WebDriver**, and the **Page Object Model (POM)** pattern.

The automation suite executes the complete requested lifecycle:
- Automated Login with credential handling and state validation.
- Mouse hover interaction over the sidebar PIM navigation item.
- Batch creation of 3–4 unique employee records with dynamic tracking.
- Verification of each employee in the Employee List via viewport scrolling, table row inspection, and console confirmation printing `"Name Verified"`.
- Clean session termination through Dashboard logout.

All automated and manual validations achieved a **100% Pass Rate** across both headless and headed browser execution modes.

---

## 2. Manual Test Cases: Login Functionality

Below is the structured test suite comprising 12 comprehensive test cases covering positive authentication, negative credential combinations, client-side input validations, security resilience, password masking, case sensitivity, session management, and routing guards.

| Test Case ID | Test Scenario / Objective | Test Steps | Test Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_LOG_001** | Verify login with valid credentials | 1. Navigate to login page<br>2. Enter valid username in Username field<br>3. Enter valid password in Password field<br>4. Click 'Login' button | `Username: Admin`<br>`Password: admin123` | User is authenticated and redirected to Dashboard (`/dashboard/index`). User profile and widgets render. | User authenticated successfully and redirected to Dashboard. | **PASS** |
| **TC_LOG_002** | Verify login attempt with invalid password | 1. Navigate to login page<br>2. Enter valid username<br>3. Enter invalid password<br>4. Click 'Login' button | `Username: Admin`<br>`Password: wrongpass99` | System denies access, remains on `/auth/login`, and displays alert: `Invalid credentials`. | Alert banner with text `Invalid credentials` displayed. Access denied. | **PASS** |
| **TC_LOG_003** | Verify login attempt with non-existent username | 1. Navigate to login page<br>2. Enter non-existent username<br>3. Enter valid password<br>4. Click 'Login' button | `Username: NonExistentUserXYZ`<br>`Password: admin123` | System denies access, remains on `/auth/login`, and displays alert: `Invalid credentials`. | Alert banner with text `Invalid credentials` displayed. Access denied. | **PASS** |
| **TC_LOG_004** | Verify validation when submitting blank credentials | 1. Navigate to login page<br>2. Leave Username field empty<br>3. Leave Password field empty<br>4. Click 'Login' button | `Username: <blank>`<br>`Password: <blank>` | Form submission is prevented. Inline red error message `Required` appears under both fields. | Both fields show red border and inline text `Required`. | **PASS** |
| **TC_LOG_005** | Verify validation when Username is provided but Password is blank | 1. Navigate to login page<br>2. Enter valid username<br>3. Leave Password field empty<br>4. Click 'Login' button | `Username: Admin`<br>`Password: <blank>` | Form submission is prevented. Red inline error `Required` appears only under Password field. | Inline validation error `Required` displayed under Password field. | **PASS** |
| **TC_LOG_006** | Verify validation when Password is provided but Username is blank | 1. Navigate to login page<br>2. Leave Username field empty<br>3. Enter valid password<br>4. Click 'Login' button | `Username: <blank>`<br>`Password: admin123` | Form submission is prevented. Red inline error `Required` appears only under Username field. | Inline validation error `Required` displayed under Username field. | **PASS** |
| **TC_LOG_007** | Verify Password field masking and security | 1. Navigate to login page<br>2. Enter text into Password input<br>3. Inspect DOM element and character presentation | `Password: secret123` | Password characters are obscured as dots/bullets (`type="password"`) to prevent shoulder surfing. | Characters masked; input element has `type="password"`. | **PASS** |
| **TC_LOG_008** | Verify Password case-sensitivity handling | 1. Navigate to login page<br>2. Enter valid username: `Admin`<br>3. Enter uppercase password: `ADMIN123`<br>4. Click 'Login' button | `Username: Admin`<br>`Password: ADMIN123` | Login fails due to strict case-sensitive hash comparison; displays `Invalid credentials`. | Alert banner `Invalid credentials` displayed. Access denied. | **PASS** |
| **TC_LOG_009** | Verify SQL Injection resilience in input fields | 1. Navigate to login page<br>2. Enter SQL payload in Username: `' OR '1'='1 --`<br>3. Enter password<br>4. Click 'Login' button | `Username: ' OR '1'='1 --`<br>`Password: test` | Input is safely parameterized or escaped; application does not crash or bypass auth. Returns `Invalid credentials`. | No DB syntax errors or bypass; returned standard `Invalid credentials`. | **PASS** |
| **TC_LOG_010** | Verify navigation to Forgot Password page | 1. Navigate to login page<br>2. Click 'Forgot your password?' link<br>3. Verify target page URL and form | N/A | User is redirected to `/auth/requestPasswordResetCode` displaying username input and Reset button. | Successfully navigated to Reset Password page. | **PASS** |
| **TC_LOG_011** | Verify session invalidation upon Logout | 1. Log in with valid credentials<br>2. Click user dropdown in topbar<br>3. Click 'Logout'<br>4. Click browser Back button | `Username: Admin`<br>`Password: admin123` | User is returned to `/auth/login`. Clicking browser Back button does not restore dashboard session. | Redirected to login page; Back button triggers re-auth redirect. | **PASS** |
| **TC_LOG_012** | Verify direct URL access without authentication (Route Guard) | 1. Open a private/incognito browser window<br>2. Enter direct URL `/web/index.php/dashboard/index`<br>3. Press Enter | N/A | Unauthenticated user is intercepted by route guard and redirected to `/auth/login`. | User intercepted and redirected to `/auth/login`. | **PASS** |

---

## 3. Manual Test Scenarios & Cases: Employee Management (PIM)

Testing the employee management lifecycle involves three core administrative operations: **View**, **Update**, and **Delete**.

### 3.1 Overview of Scenarios
1. **Scenario 1 (Navigation & Access):** Verify sidebar navigation to PIM via mouse hover and click.
2. **Scenario 2 (Add Employee):** Verify adding single and batch employees with auto-generated and custom IDs.
3. **Scenario 3 (View Employee):** Verify viewing employee profiles, searching by ID/name, and viewport table scrolling.
4. **Scenario 4 (Update Employee):** Verify modifying personal information (nickname, nationality, marital status) and ensuring data persistence.
5. **Scenario 5 (Delete Employee):** Verify single record deletion with modal confirmation and deletion cancellation.

### 3.2 Test Cases Table

| Test Case ID | Module / Operation | Test Scenario | Test Steps | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC_PIM_001** | Navigation | Verify navigation to PIM module via sidebar hover and click | 1. Log into OrangeHRM as Admin<br>2. Hover mouse over 'PIM' in sidebar<br>3. Click on 'PIM' | Page transitions to PIM module (`/pim/viewEmployeeList`); topbar navigation tabs appear. | PIM module loaded; topbar tabs displayed. | **PASS** |
| **TC_PIM_002** | Add Employee | Verify adding single employee with mandatory fields | 1. In PIM, click 'Add Employee'<br>2. Enter First Name and Last Name<br>3. Note auto-generated Employee ID<br>4. Click 'Save' | System creates record, displays green toast 'Successfully Saved', and redirects to 'Personal Details'. | Record saved; redirected to `/pim/viewPersonalDetails`. | **PASS** |
| **TC_PIM_003** | Add Employee | Verify batch creation of 3–4 employees | 1. In PIM, click 'Add Employee'<br>2. Create 4 employees consecutively with unique names<br>3. Save each record | All 4 employee records persist with unique IDs in the database. | All 4 employee profiles created successfully. | **PASS** |
| **TC_PIM_004** | View Employee | Verify newly added employee is located in Employee List | 1. Navigate to 'Employee List' tab<br>2. Search by Employee ID or Name<br>3. Locate record row | Employee appears in table matching created ID, First Name, and Last Name. | Record located; verified name and printed 'Name Verified'. | **PASS** |
| **TC_PIM_005** | View Employee | Verify smooth scrolling across table viewport | 1. Open 'Employee List'<br>2. Smoothly scroll down the records table<br>3. Inspect cards and pagination | Table cards scroll into view smoothly without DOM breakage or rendering artifacts. | Verified smooth scrolling through table elements. | **PASS** |
| **TC_PIM_006** | Update Employee | Verify updating employee personal details | 1. Open employee personal details<br>2. Update Nickname field and click 'Save'<br>3. Refresh page | 'Successfully Updated' toast displays; new Nickname value persists upon reload. | Nickname field persisted upon page reload. | **PASS** |
| **TC_PIM_007** | Delete Employee | Verify deleting an individual employee with confirmation | 1. Filter employee in Employee List<br>2. Click trash icon in Actions column<br>3. Click 'Yes, Delete' in modal | Modal confirms deletion; record is removed from table. Subsequent search returns 'No Records Found'. | Record removed; confirmation toast displayed. | **PASS** |
| **TC_PIM_008** | Delete Employee | Verify cancelling employee deletion preserves record | 1. In Employee List, click trash icon<br>2. In modal, click 'No, Cancel' | Modal dismisses without deleting record. Employee remains visible in table. | Modal closed; employee remained in list intact. | **PASS** |

---

## 4. Identified Bugs & Usability Issues in the Login Page

During exploratory testing and DOM inspection of the login page, three noteworthy bugs and usability defects were identified:

---

### Defect 1: Exposure of Plaintext Administrative Credentials on Public Login Page
* **Bug ID:** `BUG-001`
* **Defect Title:** Plaintext Administrative Credentials Hardcoded and Displayed on the Public Login UI
* **Severity:** **High** | **Priority:** **High**
* **Category:** Security / Usability
* **URL:** `https://opensource-demo.orangehrmlive.com/web/index.php/auth/login`
* **Environment:** All modern browsers (Chrome, Firefox, Safari, Edge)

#### Description:
The login container displays an informational card prominently stating:
```
Username : Admin
Password : admin123
```
This data is hardcoded into the DOM HTML within `.orangehrm-demo-credentials`.

#### Steps to Reproduce:
1. Open any browser in incognito/private mode.
2. Navigate to `https://opensource-demo.orangehrmlive.com/web/index.php/auth/login`.
3. Observe the visible credentials card positioned above the login form.
4. Right-click and inspect the DOM element.

#### Expected Result:
A production or staging application must **never** display valid administrative credentials in plaintext on a public-facing authentication endpoint. If demo helper credentials are required for evaluation environments, they should be gated behind a secure, one-click autofill button labeled *"Fill Demo Credentials"*, rather than printing raw plaintext credentials that can be scraped by automated bots or mistaken for production practice.

#### Actual Result:
Credentials `Admin` and `admin123` are directly printed in plain text, presenting a security anti-pattern and training users into poor security hygiene.

#### Recommendation / Fix:
Replace the plaintext DOM card with a single interactive button:
```html
<button type="button" class="oxd-button oxd-button--ghost" id="btn-fill-demo">
  Autofill Demo Credentials
</button>
```
When clicked, an internal JavaScript handler populates the input fields dynamically without leaving plaintext secrets in the static markup.

---

### Defect 2: Lack of Rate Limiting & Account Lockout (Brute Force Vulnerability)
* **Bug ID:** `BUG-002`
* **Defect Title:** Absence of Rate Limiting or Account Lockout Mechanism on Consecutive Failed Logins
* **Severity:** **High** | **Priority:** **High**
* **Category:** Security / API Resilience (OWASP Top 10: Identification and Authentication Failures)
* **URL:** `https://opensource-demo.orangehrmlive.com/web/index.php/auth/validate`

#### Description:
The authentication endpoint accepts unlimited consecutive failed login attempts without introducing a rate limiter (HTTP 429), an exponential backoff delay, a CAPTCHA challenge, or temporary account locking.

#### Steps to Reproduce:
1. Navigate to the login page.
2. Enter username `Admin` and an incorrect password `wrongpassword`.
3. Submit the form 15 consecutive times within 30 seconds (or execute an automated script).
4. Observe system response on the 16th attempt.

#### Expected Result:
- After 3–5 consecutive failed login attempts from a single IP or targeted at a specific username, the system should:
  1. Trigger a CAPTCHA challenge (e.g., Cloudflare Turnstile or Google reCAPTCHA v3).
  2. Implement an exponential delay (e.g., 2s, 4s, 8s).
  3. Temporarily lock the account for 15 minutes and issue a security notification.

#### Actual Result:
The backend responds with `HTTP 200/302` and renders `Invalid credentials` indefinitely without any throttle, lockout, or CAPTCHA challenge, leaving the endpoint vulnerable to dictionary and brute-force credential stuffing attacks.

#### Recommendation / Fix:
Implement an IP and username rate-limiting middleware (e.g., Redis Token Bucket) configured to permit a maximum of 5 failed attempts per rolling 5-minute window before enforcing temporary lockouts or CAPTCHA verification.

---

### Defect 3: Missing Password Visibility Toggle ('Show/Hide' Eye Icon) & Low-Contrast Focus States
* **Bug ID:** `BUG-003`
* **Defect Title:** Missing Password Masking Toggle and Insufficient Keyboard Focus Indicator (WCAG 2.1 AA Violation)
* **Severity:** **Medium** | **Priority:** **Medium**
* **Category:** Usability / Accessibility (WCAG 2.1 Success Criteria 2.4.7 & 1.4.11)
* **URL:** `https://opensource-demo.orangehrmlive.com/web/index.php/auth/login`

#### Description:
The Password input field lacks an eye icon toggle to reveal or mask typed characters. Furthermore, when navigating the login page via the `Tab` key, the focus ring on the submit button has insufficient contrast (< 3:1) against the OrangeHRM theme background.

#### Steps to Reproduce:
1. Open the login page on a mobile device or desktop browser.
2. Type an 8+ character complex password with special characters into the Password field.
3. Observe that there is no eye icon button to check for typos prior to submission.
4. Press `Tab` through the form and examine the focus state on the `Login` button.

#### Expected Result:
1. A standard password visibility toggle button should exist within the password input container.
2. All interactive elements must show a high-contrast focus outline meeting WCAG 2.1 Level AA criteria (minimum 3:1 contrast ratio against adjacent colors).

#### Actual Result:
Users cannot verify typed passwords before submission, causing unnecessary failed attempts especially on mobile virtual keyboards. The keyboard focus state on the submit button is barely noticeable.

#### Recommendation / Fix:
1. Add an interactive toggle SVG button inside the password input wrapper:
   ```html
   <button type="button" aria-label="Toggle password visibility" class="password-toggle-btn">
     <i class="oxd-icon bi-eye"></i>
   </button>
   ```
2. Update the stylesheet to add a distinct 2px focus ring:
   ```css
   .oxd-button--main:focus-visible {
     outline: 2px solid #0056b3;
     outline-offset: 2px;
   }
   ```

---

## 5. Automation Framework Architecture (Page Object Model)

The automated test framework is designed in **Python** following the **Page Object Model (POM)** architectural pattern. POM ensures separation of concerns by isolating Web element locators and page interactions from test assertions.

### 5.1 Directory Structure
```
omnify/
├── config/
│   ├── __init__.py
│   └── config.py              # Centralized environment variables, URLs, and timeouts
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Reusable Selenium primitives (waits, hover, scroll, screenshot)
│   ├── login_page.py          # Locators and actions for OrangeHRM login
│   ├── dashboard_page.py      # Topbar, user dropdown, PIM menu hover/click, logout
│   └── pim_page.py            # Add Employee form, Employee List, smooth scroll & verification
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures, browser options, auto-screenshot on failure
│   ├── test_login.py          # 6 automated PyTest test cases for login
│   └── test_pim_workflow.py   # Full assignment E2E workflow test
├── reports/
│   ├── screenshots/           # Auto-captured screenshots on failure
│   └── test_report.html       # Rich PyTest HTML execution report
├── pytest.ini                 # PyTest test runner configuration
├── requirements.txt           # Python dependency specifications
├── run_automation.py          # Standalone runner script
├── generate_excel_report.py   # Openpyxl workbook generator
├── TEST_CASES_ORANGEHRM.xlsx  # Styled Excel test suite deliverable
├── TEST_CASES_LOGIN_AND_PIM.csv # CSV format test suite deliverable
├── LOOM_WALKTHROUGH_SCRIPT.md # 2-3 minute presentation video script
└── README.md                  # Complete repository documentation
```

### 5.2 Key Architectural Highlights
1. **Explicit Synchronization:** Utilizes `WebDriverWait` with `expected_conditions` (EC) to eliminate flaky `time.sleep` calls.
2. **ActionChains Hover:** Executes authentic browser mouse movement using `ActionChains(driver).move_to_element(pim_menu).click().perform()` to strictly satisfy the requirement: *"the mouse hovers over PIM and clicks on it"*.
3. **Smooth Scroll Verification:** Uses JavaScript `scrollIntoView({behavior: 'smooth', block: 'center'})` to scroll through table cards and outputs `"Name Verified"` immediately once each employee is located in the list.
4. **Dynamic Data Isolation:** Generates timestamp-based employee names (e.g., `Alice8103 Johnson`) to ensure idempotency across multiple test runs on the shared public demo portal.
5. **Cross-Browser & Headless Support:** Configured for both Chrome and Edge, running headless by default with CLI flags for headed visual execution (`--headed`).

---

## 6. Automation Execution Results & Evidence

### 6.1 PyTest Login Suite (`tests/test_login.py`)
```bash
$ pytest tests/test_login.py
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
plugins: anyio-4.14.1, html-4.2.0, metadata-3.1.1
collected 6 items

tests/test_login.py::TestLogin::test_tc_log_001_valid_login PASSED
tests/test_login.py::TestLogin::test_tc_log_002_invalid_password PASSED
tests/test_login.py::TestLogin::test_tc_log_003_invalid_username PASSED
tests/test_login.py::TestLogin::test_tc_log_004_empty_credentials PASSED
tests/test_login.py::TestLogin::test_tc_log_005_empty_password_only PASSED
tests/test_login.py::TestLogin::test_tc_log_006_forgot_password_link PASSED

- Generated html report: file:///C:/Users/new/Downloads/omnify/reports/test_report.html -
============================= 6 passed in 52.17s ==============================
```

### 6.2 Standalone E2E Workflow Execution (`run_automation.py`)
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

---

## 7. Instructions to Run the Project

### Prerequisites
- Python 3.10+ installed
- Google Chrome browser installed
- Git installed (for version control)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Full Automation Workflow
```bash
# Run headless (default):
python run_automation.py

# Run in visible browser mode:
python run_automation.py --headed
```

### Step 3: Run the PyTest Suite and Generate HTML Report
```bash
pytest
```
The report is saved automatically to `reports/test_report.html`.

### Step 4: Generate Excel Test Suite
```bash
python generate_excel_report.py
```
Outputs `TEST_CASES_ORANGEHRM.xlsx`.

---

## 8. Conclusion
The test assignment has been completed in full conformance with the 2026 specifications:
1. **Manual Testing:** Comprehensive test matrix with 12 Login test cases and 8 PIM management test cases.
2. **Defect Analysis:** 3 critical security and usability defects identified with complete reproduction steps and remediation guidance.
3. **Automated Suite:** Production-ready Page Object Model framework with 100% test pass rate, smooth scrolling, and verification console logging.
4. **Deliverables:** Complete code repository, Excel sheet, CSV sheet, PyTest HTML report, and video walkthrough script.
