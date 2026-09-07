"""
Automated End-to-End Workflow Test for OrangeHRM:
1. Automate the Login Flow.
2. Navigate to PIM module: Mouse hovers over PIM and clicks on it.
3. Add Employees: On the PIM page, click on 'Add Employee' and add 3-4 employees.
4. Verify Employees in the Employee List:
   - Navigate to 'Employee List' page.
   - Scroll through the list and locate the employees added.
   - Verify their names and print 'Name Verified' once found.
5. Log Out from the Dashboard.
"""
import time
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage
from config.config import Config


class TestPimWorkflow:
    """End-to-End PIM Workflow Automation Test Suite."""

    def test_e2e_pim_employee_lifecycle(self, driver):
        """
        Executes the complete assignment workflow:
        Login -> Hover & Click PIM -> Add 3-4 Employees -> Verify with Scrolling & Print -> Logout
        """
        # ==========================================
        # STEP 1: AUTOMATE LOGIN FLOW
        # ==========================================
        print("\n" + "="*70)
        print("STEP 1: Logging into OrangeHRM...")
        print("="*70)
        login_page = LoginPage(driver).load()
        login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_dashboard_displayed(), "Login failed: Dashboard not displayed!"
        print(f"-> Login successful. User: {dashboard_page.get_user_name()}")

        # ==========================================
        # STEP 2: NAVIGATE TO PIM MODULE (HOVER & CLICK)
        # ==========================================
        print("\n" + "="*70)
        print("STEP 2: Navigating to PIM Module (Hover and Click)...")
        print("="*70)
        dashboard_page.hover_and_click_pim()
        pim_page = PimPage(driver)
        assert "/pim/viewEmployeeList" in driver.current_url, "Failed to navigate to PIM module!"
        print("-> Successfully hovered over PIM and navigated to PIM Module.")

        # ==========================================
        # STEP 3: ADD 3-4 EMPLOYEES
        # ==========================================
        print("\n" + "="*70)
        print("STEP 3: Adding Employees to OrangeHRM...")
        print("="*70)
        batch_id = int(time.time()) % 10000

        employees_to_add = [
            {"first": f"Alice{batch_id}", "middle": "M", "last": "Johnson"},
            {"first": f"Bob{batch_id}", "middle": "K", "last": "Smith"},
            {"first": f"Carol{batch_id}", "middle": "R", "last": "Williams"},
            {"first": f"David{batch_id}", "middle": "L", "last": "Brown"}
        ]

        added_employees = []
        for idx, emp in enumerate(employees_to_add, start=1):
            print(f"-> Adding Employee #{idx}: {emp['first']} {emp['last']}")
            added_info = pim_page.add_employee(
                first_name=emp["first"],
                last_name=emp["last"],
                middle_name=emp["middle"]
            )
            added_employees.append(added_info)
            print(f"   Saved Employee #{idx}: {added_info['first_name']} {added_info['last_name']} (Emp ID: {added_info['emp_id']})")
            time.sleep(1)

        assert len(added_employees) == len(employees_to_add), "Not all employees were added successfully!"
        print(f"-> All {len(added_employees)} employees added successfully.")

        # ==========================================
        # STEP 4: VERIFY EMPLOYEES IN EMPLOYEE LIST
        # ==========================================
        print("\n" + "="*70)
        print("STEP 4: Verifying Employees in Employee List...")
        print("="*70)

        verified_count = 0
        for emp in added_employees:
            print(f"-> Locating employee in list: {emp['first_name']} {emp['last_name']} (ID: {emp['emp_id']})")
            
            # Navigate to list and verify with smooth scrolling
            is_verified = pim_page.locate_and_verify_employee_in_list(
                first_name=emp["first_name"],
                last_name=emp["last_name"],
                emp_id=emp["emp_id"]
            )
            if is_verified:
                verified_count += 1
            time.sleep(1)

        assert verified_count == len(added_employees), f"Expected {len(added_employees)} verified employees, but got {verified_count}"
        print(f"-> All {verified_count} employees successfully located and verified with 'Name Verified' printed.")

        # ==========================================
        # STEP 5: LOG OUT FROM THE DASHBOARD
        # ==========================================
        print("\n" + "="*70)
        print("STEP 5: Logging out from OrangeHRM...")
        print("="*70)
        dashboard_page.logout()
        assert login_page.is_login_page_displayed(), "Logout failed: Login page not displayed!"
        print("-> Successfully logged out from the Dashboard. Redirected to Login page.")
        print("="*70)
        print("ALL WORKFLOW STEPS COMPLETED SUCCESSFULLY!")
        print("="*70)
