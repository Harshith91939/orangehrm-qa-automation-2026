# 2-3 Minute Loom Video Walkthrough Script

**Video Title:** QA Engineer Assignment Walkthrough – OrangeHRM Manual & Automation Suite  
**Target Duration:** 2 minutes 30 seconds (150 seconds)  
**Presenter:** QA Automation Engineer  

---

## Preparation Checklist Before Recording
- [ ] Have VS Code / your IDE open showing the `omnify` project directory.
- [ ] Open `QA_ASSIGNMENT_REPORT.md` or `TEST_CASES_ORANGEHRM.xlsx` in one window.
- [ ] Have your terminal ready with `python run_automation.py --headed` typed and paused.
- [ ] Open `reports/test_report.html` in Chrome ready to show.
- [ ] Test your microphone and ensure clean desktop background.

---

## Timeline & Speaking Script

```
+-------------------------------------------------------------------------------+
|  TIMELINE OVERVIEW                                                            |
|  0:00 - 0:25  (25s): Introduction, Objective, and Scope                       |
|  0:25 - 1:00  (35s): Manual Test Cases & 3 Identified Bugs/Usability Issues   |
|  1:00 - 1:45  (45s): Automation Framework Architecture (Page Object Model)    |
|  1:45 - 2:15  (30s): Live Test Execution & Verification Evidence              |
|  2:15 - 2:30  (15s): Deliverables Summary & Closing                           |
+-------------------------------------------------------------------------------+
```

---

### [0:00 – 0:25] Segment 1: Introduction & Objective
* **Screen Display:** Project folder in IDE and title of `QA_ASSIGNMENT_REPORT.md`.
* **Talking Points:**
> *"Hello everyone! My name is [Your Name], and today I am walking you through my QA Engineer Assignment for the OrangeHRM web portal.*
>
> *The assignment focuses on two core areas:*
> 1. *A comprehensive manual QA analysis of the Login functionality and PIM employee management lifecycle (view, update, delete).*
> 2. *A modular, robust automation suite built in Python using Selenium WebDriver, PyTest, and the Page Object Model design pattern.*
>
> *Let's jump right into the manual test design and bug analysis."*

---

### [0:25 – 1:00] Segment 2: Manual Test Cases & Identified Bugs
* **Screen Display:** Scroll to Section 2 and Section 4 of `QA_ASSIGNMENT_REPORT.md` (or show `TEST_CASES_ORANGEHRM.xlsx`).
* **Talking Points:**
> *"For the Login functionality, I authored 12 comprehensive test cases covering positive authentication, invalid password and username permutations, blank input validations, SQL injection resilience, and session invalidation upon logout.*
>
> *During exploratory testing, I identified three critical bugs and usability issues:*
> 1. *First, **Exposure of Plaintext Administrative Credentials on the Public Login Page**—rendering credentials in raw DOM is a severe security anti-pattern.*
> 2. *Second, **Lack of Rate Limiting or Account Lockout**—the endpoint allows unlimited rapid failed login attempts without CAPTCHA or backoff delays, making it vulnerable to brute-force attacks.*
> 3. *Third, **Missing Password Visibility Toggle and Low-Contrast Focus States**—violating WCAG 2.1 accessibility standards and creating friction for users."*

---

### [1:00 – 1:45] Segment 3: Automation Framework Architecture (POM)
* **Screen Display:** Expand folder tree in VS Code (`config/`, `pages/`, `tests/`, `reports/`).
* **Talking Points:**
> *"Now turning to the automation framework: I structured the project strictly around the **Page Object Model**.*
>
> *Under `pages/`:*
> - *`base_page.py` encapsulates reusable Selenium primitives, explicit waits, screenshots, and smooth scrolling.*
> - *`login_page.py` manages all login locators and form submissions.*
> - *`dashboard_page.py` handles topbar navigation, user profile checks, and logout.*
> - *`pim_page.py` implements the employee creation flow, search filters, and table inspection.*
>
> *In `tests/`:*
> - *`test_login.py` runs 6 automated PyTest validation scenarios.*
> - *`test_pim_workflow.py` executes the required end-to-end flow: logging in, hovering over PIM using ActionChains, adding 4 employees, smoothly scrolling the employee table, printing `'Name Verified'`, and logging out."*

---

### [1:45 – 2:15] Segment 4: Live Test Execution & Console Verification
* **Screen Display:** Terminal window running `python run_automation.py` (or displaying the test output) + open `reports/test_report.html`.
* **Talking Points:**
> *"Let's take a look at the live execution output.*
>
> *As you can see in the terminal:*
> - *Step 1: Admin logs in successfully.*
> - *Step 2: Mouse hovers over PIM and clicks through to the module.*
> - *Step 3: Four unique employees—Alice, Bob, Carol, and David—are created with distinct system IDs.*
> - *Step 4: The script navigates to the Employee List, smoothly scrolls through the table, locates each employee, and outputs **'Name Verified'** for each person.*
> - *Step 5: Finally, the script terminates the session via dashboard logout.*
>
> *Additionally, running `pytest` produces this interactive HTML execution report showing a 100% pass rate."*

---

### [2:15 – 2:30] Segment 5: Deliverables & Conclusion
* **Screen Display:** Quick view of the GitHub repository files (`README.md`, `TEST_CASES_ORANGEHRM.xlsx`).
* **Talking Points:**
> *"All artifacts—including the full source code, Excel test suite, CSV file, HTML report, and detailed QA markdown report—are committed to this GitHub repository.*
>
> *Thank you very much for your time and review. I look forward to discussing my technical approach in the next stage!"*

---

## Pro-Tips for Recording
1. Keep your pace steady and enthusiastic.
2. Highlight your mouse cursor so viewers can follow the files and terminal lines easily.
3. If using Loom, enable the small circular webcam bubble in the corner.
4. Keep the duration strictly between **2:15 and 2:45 minutes**.
