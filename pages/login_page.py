"""
Page Object representing the OrangeHRM Login Page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """Encapsulates locators and actions for the Login Page."""

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ALERT_ERROR = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    INPUT_ERROR_MSG = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[contains(@class, 'orangehrm-login-forgot-header')]")
    COMPANY_LOGO = (By.CSS_SELECTOR, "img[alt='company-branding']")
    LOGIN_TITLE = (By.CSS_SELECTOR, "h5.orangehrm-login-title")

    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        """Open the OrangeHRM login page."""
        self.open(Config.BASE_URL)
        self.wait_for_visibility(self.USERNAME_INPUT)
        return self

    def enter_username(self, username):
        """Input username into username field."""
        self.send_keys(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        """Input password into password field."""
        self.send_keys(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click on the Login submit button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        """Perform end-to-end login action."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Retrieve invalid credentials alert banner message."""
        return self.get_text(self.ALERT_ERROR)

    def get_field_validation_errors(self):
        """Retrieve any inline 'Required' validation messages."""
        elements = self.wait_for_all_visible(self.INPUT_ERROR_MSG, timeout=5)
        return [el.text.strip() for el in elements]

    def click_forgot_password(self):
        """Click the 'Forgot your password?' link."""
        self.click(self.FORGOT_PASSWORD_LINK)

    def is_login_page_displayed(self):
        """Check if login page components are rendered."""
        return (
            self.is_displayed(self.USERNAME_INPUT) and
            self.is_displayed(self.PASSWORD_INPUT) and
            self.is_displayed(self.LOGIN_BUTTON)
        )
