"""
Page Object representing the OrangeHRM PIM (Personnel Information Management) Module.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import Config


class PimPage(BasePage):
    """Encapsulates locators and workflows for Employee Management in PIM."""

    # Topbar Navigation Tabs
    TAB_EMPLOYEE_LIST = (By.XPATH, "//a[text()='Employee List']")
    TAB_ADD_EMPLOYEE = (By.XPATH, "//a[text()='Add Employee']")
    TAB_REPORTS = (By.XPATH, "//a[text()='Reports']")

    # Add Employee Form Locators
    INPUT_FIRST_NAME = (By.NAME, "firstName")
    INPUT_MIDDLE_NAME = (By.NAME, "middleName")
    INPUT_LAST_NAME = (By.NAME, "lastName")
    INPUT_EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/parent::div/following-sibling::div/input")
    BTN_SAVE = (By.CSS_SELECTOR, "button[type='submit']")
    BTN_CANCEL = (By.XPATH, "//button[normalize-space()='Cancel']")
    TOAST_SUCCESS = (By.CSS_SELECTOR, ".oxd-toast-content--success")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[text()='Personal Details']")

    # Employee List / Search Locators
    SEARCH_EMP_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
    SEARCH_EMP_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/parent::div/following-sibling::div/input")
    BTN_SEARCH = (By.CSS_SELECTOR, "button[type='submit']")
    BTN_RESET = (By.XPATH, "//button[normalize-space()='Reset']")
    TABLE_CONTAINER = (By.CSS_SELECTOR, ".oxd-table-body")
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-card")
    RECORDS_FOUND_TEXT = (By.XPATH, "//span[contains(., 'Record')]")

    # Confirmation Modal
    CONFIRM_DELETE_BTN = (By.CSS_SELECTOR, ".oxd-button--label-danger")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_add_employee(self):
        """Click on 'Add Employee' top navigation tab."""
        self.click(self.TAB_ADD_EMPLOYEE)
        self.wait_for_url_contains(Config.ADD_EMP_URL_SUBSTRING)
        self.wait_for_visibility(self.INPUT_FIRST_NAME)

    def navigate_to_employee_list(self):
        """Click on 'Employee List' top navigation tab."""
        self.click(self.TAB_EMPLOYEE_LIST)
        self.wait_for_url_contains(Config.PIM_URL_SUBSTRING)
        self.wait_for_visibility(self.SEARCH_EMP_ID_INPUT)

    def add_employee(self, first_name, last_name, middle_name="", custom_id=None):
        """
        Fill and submit the Add Employee form.
        Returns a dict containing the employee details including assigned ID.
        """
        self.navigate_to_add_employee()
        
        self.send_keys(self.INPUT_FIRST_NAME, first_name)
        if middle_name:
            self.send_keys(self.INPUT_MIDDLE_NAME, middle_name)
        self.send_keys(self.INPUT_LAST_NAME, last_name)

        if custom_id:
            self.send_keys(self.INPUT_EMPLOYEE_ID, custom_id)
            emp_id = custom_id
        else:
            emp_id = self.get_attribute(self.INPUT_EMPLOYEE_ID, "value")

        self.click(self.BTN_SAVE)

        # Wait for either personal details page or success toast
        self.wait_for_url_contains("/pim/viewPersonalDetails", timeout=20)
        
        return {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "emp_id": emp_id
        }

    def search_by_employee_id(self, emp_id):
        """Search employee by ID in Employee List."""
        self.send_keys(self.SEARCH_EMP_ID_INPUT, emp_id)
        self.click(self.BTN_SEARCH)
        time.sleep(1.5)  # Wait for table reload

    def search_by_employee_name(self, name):
        """Search employee by Name in Employee List."""
        self.send_keys(self.SEARCH_EMP_NAME_INPUT, name)
        self.click(self.BTN_SEARCH)
        time.sleep(1.5)

    def reset_search_filters(self):
        """Reset search form."""
        self.click(self.BTN_RESET)
        time.sleep(1)

    def locate_and_verify_employee_in_list(self, first_name, last_name, emp_id=None):
        """
        Scroll through the list, locate the employee, verify their name,
        and print 'Name Verified' once found.
        """
        self.navigate_to_employee_list()
        
        # If emp_id is given, filter by ID to ensure row is readily displayed
        if emp_id:
            self.search_by_employee_id(emp_id)

        rows = self.wait_for_all_visible(self.TABLE_ROWS, timeout=10)
        found = False

        for row in rows:
            # Scroll smoothly to each row
            self.scroll_to_element(row)
            row_text = row.text
            
            # Check if name is present in row
            if first_name in row_text and last_name in row_text:
                found = True
                print(f"[VERIFICATION SUCCESS] Located Employee: {first_name} {last_name} (ID: {emp_id})")
                print("Name Verified")
                break

        assert found, f"Employee '{first_name} {last_name}' (ID: {emp_id}) was not found in the list!"
        return True

    def delete_employee_by_id(self, emp_id):
        """Delete an employee row by filtering their ID."""
        self.navigate_to_employee_list()
        self.search_by_employee_id(emp_id)
        
        # Find trash bin icon inside the table row
        trash_btn = (By.CSS_SELECTOR, "button i.bi-trash")
        self.click(trash_btn)
        
        # Confirm deletion dialog
        self.click(self.CONFIRM_DELETE_BTN)
        time.sleep(1.5)
