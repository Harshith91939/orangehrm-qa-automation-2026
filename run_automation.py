"""
Standalone Runner Script for OrangeHRM POM Automation Suite.
Executes the full QA assignment workflow cleanly.

Usage:
    python run_automation.py
    python run_automation.py --headed
"""
import sys
import os
import argparse
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage
from config.config import Config


def run_pipeline(headless=True):
    print("=" * 80)
    print("  ORANGEHRM AUTOMATION WORKFLOW - PAGE OBJECT MODEL (POM)")
    print(f"  Browser: Headless={headless} | Target URL: {Config.BASE_URL}")
    print("=" * 80)

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    try:
        # 1. Automate the Login Flow
        print("\n[STEP 1/5] Automating Login Flow...")
        login_page = LoginPage(driver).load()
        login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_dashboard_displayed(), "Login failed: Dashboard not loaded."
        print(f"SUCCESS: Logged in successfully as '{dashboard_page.get_user_name()}'.")

        # 2. Navigate to PIM module: mouse hovers over PIM and clicks on it
        print("\n[STEP 2/5] Navigating to PIM Module (Mouse Hover & Click)...")
        dashboard_page.hover_and_click_pim()
        pim_page = PimPage(driver)
        print("SUCCESS: Hovered over PIM menu item and navigated to PIM Module.")

        # 3. Add Employees: On the PIM page, click on 'Add Employee' and add 3-4 employees
        print("\n[STEP 3/5] Adding 3-4 Employees in PIM Module...")
        batch_id = int(time.time()) % 10000
        employees_to_create = [
            {"first": f"Alice{batch_id}", "middle": "M", "last": "Johnson"},
            {"first": f"Bob{batch_id}", "middle": "K", "last": "Smith"},
            {"first": f"Carol{batch_id}", "middle": "R", "last": "Williams"},
            {"first": f"David{batch_id}", "middle": "L", "last": "Brown"}
        ]

        created_employees = []
        for i, emp_data in enumerate(employees_to_create, start=1):
            print(f"   -> Creating Employee {i}/{len(employees_to_create)}: {emp_data['first']} {emp_data['last']}...")
            info = pim_page.add_employee(
                first_name=emp_data["first"],
                last_name=emp_data["last"],
                middle_name=emp_data["middle"]
            )
            created_employees.append(info)
            print(f"      Saved: {info['first_name']} {info['last_name']} (Employee ID: {info['emp_id']})")
            time.sleep(1)

        print(f"SUCCESS: Total {len(created_employees)} employees added to OrangeHRM.")

        # 4. Verify Employees in the Employee List:
        # Navigate to "Employee List" page, scroll through list, locate employees, verify names and print "Name Verified"
        print("\n[STEP 4/5] Verifying Employees in Employee List...")
        for emp in created_employees:
            print(f"   -> Checking Employee: {emp['first_name']} {emp['last_name']} (ID: {emp['emp_id']})...")
            pim_page.locate_and_verify_employee_in_list(
                first_name=emp["first_name"],
                last_name=emp["last_name"],
                emp_id=emp["emp_id"]
            )
            time.sleep(1)

        print("SUCCESS: All added employees located with smooth scrolling and names verified.")

        # 5. Log Out from the Dashboard
        print("\n[STEP 5/5] Logging Out from the Dashboard...")
        dashboard_page.logout()
        assert login_page.is_login_page_displayed(), "Logout failed: Login page not displayed."
        print("SUCCESS: Logged out cleanly. Returned to Login Page.")

        print("\n" + "=" * 80)
        print("  ALL 5 WORKFLOW STEPS EXECUTED AND PASSED SUCCESSFULLY!")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        # Save screenshot
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        screenshot_file = os.path.join(Config.SCREENSHOTS_DIR, f"execution_failure_{int(time.time())}.png")
        driver.save_screenshot(screenshot_file)
        print(f"Saved failure screenshot to: {screenshot_file}")
        raise
    finally:
        driver.quit()
        print("\nBrowser closed cleanly.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OrangeHRM POM Automation Runner")
    parser.add_argument("--headed", action="store_true", help="Run browser in visible (headed) mode")
    args = parser.parse_args()

    run_pipeline(headless=not args.headed)
