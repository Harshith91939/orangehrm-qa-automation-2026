"""
Page Object representing the OrangeHRM Dashboard Page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class DashboardPage(BasePage):
    """Encapsulates locators and actions for the OrangeHRM Dashboard."""

    # Locators
    HEADER_TITLE = (By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module")
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    USER_DROPDOWN_NAME = (By.CSS_SELECTOR, ".oxd-userdropdown-name")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")
    PIM_MENU_ITEM = (By.XPATH, "//span[text()='PIM']")
    SIDEBAR_MENU = (By.CSS_SELECTOR, "nav.oxd-navbar-nav")

    def __init__(self, driver):
        super().__init__(driver)

    def is_dashboard_displayed(self):
        """Verify dashboard loaded by checking header and user tab."""
        self.wait_for_url_contains(Config.DASHBOARD_URL_SUBSTRING)
        return self.is_displayed(self.USER_DROPDOWN)

    def get_user_name(self):
        """Retrieve the name of the currently logged-in user."""
        return self.get_text(self.USER_DROPDOWN_NAME)

    def hover_pim_menu(self):
        """Mouse hover over PIM sidebar menu item."""
        self.hover(self.PIM_MENU_ITEM)

    def click_pim_menu(self):
        """Click on the PIM sidebar menu item."""
        self.click(self.PIM_MENU_ITEM)

    def hover_and_click_pim(self):
        """Move mouse over PIM menu item and click it."""
        self.hover_and_click(self.PIM_MENU_ITEM)
        self.wait_for_url_contains(Config.PIM_URL_SUBSTRING)

    def logout(self):
        """Log out from OrangeHRM using user dropdown."""
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        self.wait_for_url_contains("/auth/login")
