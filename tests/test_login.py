"""
Automated tests for OrangeHRM Login Functionality.
"""
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config


class TestLogin:
    """Test suite covering Login functional workflows and validations."""

    def test_tc_log_001_valid_login(self, driver):
        """TC_LOG_001: Verify user can successfully log in with valid credentials."""
        login_page = LoginPage(driver).load()
        login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)

        dashboard_page = DashboardPage(driver)
        assert dashboard_page.is_dashboard_displayed(), "Dashboard was not displayed after valid login!"
        assert "/dashboard/index" in dashboard_page.get_current_url(), "URL does not contain dashboard path!"

    def test_tc_log_002_invalid_password(self, driver):
        """TC_LOG_002: Verify error message when logging in with invalid password."""
        login_page = LoginPage(driver).load()
        login_page.login(Config.ADMIN_USERNAME, Config.INVALID_PASSWORD)

        error_msg = login_page.get_error_message()
        assert "Invalid credentials" in error_msg, f"Expected 'Invalid credentials', got '{error_msg}'"

    def test_tc_log_003_invalid_username(self, driver):
        """TC_LOG_003: Verify error message when logging in with non-existent username."""
        login_page = LoginPage(driver).load()
        login_page.login(Config.INVALID_USERNAME, Config.ADMIN_PASSWORD)

        error_msg = login_page.get_error_message()
        assert "Invalid credentials" in error_msg, f"Expected 'Invalid credentials', got '{error_msg}'"

    def test_tc_log_004_empty_credentials(self, driver):
        """TC_LOG_004: Verify client-side required validation when submitting empty fields."""
        login_page = LoginPage(driver).load()
        login_page.click_login()

        errors = login_page.get_field_validation_errors()
        assert len(errors) >= 2, f"Expected 2 'Required' validation messages, found {len(errors)}"
        for err in errors:
            assert "Required" in err, f"Validation message '{err}' did not match 'Required'"

    def test_tc_log_005_empty_password_only(self, driver):
        """TC_LOG_005: Verify validation when entering username but leaving password empty."""
        login_page = LoginPage(driver).load()
        login_page.enter_username(Config.ADMIN_USERNAME)
        login_page.click_login()

        errors = login_page.get_field_validation_errors()
        assert len(errors) == 1, f"Expected 1 'Required' validation message, found {len(errors)}"
        assert "Required" in errors[0]

    def test_tc_log_006_forgot_password_link(self, driver):
        """TC_LOG_006: Verify 'Forgot your password?' navigates to reset password page."""
        login_page = LoginPage(driver).load()
        login_page.click_forgot_password()

        login_page.wait_for_url_contains("/requestPasswordResetCode")
        assert "/requestPasswordResetCode" in driver.current_url
