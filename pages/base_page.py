"""
Base Page Object providing reusable Selenium operations and explicit wait utilities.
"""
import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from config.config import Config


class BasePage:
    """Base class for all Page Objects in the framework."""

    def __init__(self, driver, timeout=Config.EXPLICIT_WAIT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(
            self.driver,
            timeout=self.timeout,
            poll_frequency=Config.POLL_FREQUENCY,
            ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
        )
        self.actions = ActionChains(self.driver)

    def open(self, url):
        """Navigate to a specified URL."""
        self.driver.get(url)

    def find_element(self, locator):
        """Find an element after waiting for its presence."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Find multiple elements after waiting for presence."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_visibility(self, locator, timeout=None):
        """Wait until an element is visible on the DOM."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_all_visible(self, locator, timeout=None):
        """Wait until all elements matching locator are visible."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_clickable(self, locator, timeout=None):
        """Wait until an element is clickable."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        """Click an element once it is clickable."""
        el = self.wait_for_clickable(locator)
        el.click()

    def send_keys(self, locator, text, clear_first=True):
        """Send keys to an input element after ensuring visibility."""
        el = self.wait_for_visibility(locator)
        if clear_first:
            el.click()
            # Select all and delete to handle masked inputs cleanly
            el.send_keys("\ue009a")  # Ctrl+A
            el.send_keys("\ue017")   # Delete
        el.send_keys(text)

    def get_text(self, locator):
        """Get visible text from an element."""
        return self.wait_for_visibility(locator).text.strip()

    def get_attribute(self, locator, attribute_name):
        """Get attribute value from an element."""
        el = self.wait_for_visibility(locator)
        return el.get_attribute(attribute_name)

    def is_displayed(self, locator, timeout=5):
        """Check if an element is displayed within a short timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def hover(self, locator):
        """Move mouse cursor over the specified element."""
        element = self.wait_for_visibility(locator)
        self.actions.move_to_element(element).perform()

    def hover_and_click(self, locator):
        """Move mouse cursor over the element and click it."""
        element = self.wait_for_visibility(locator)
        self.actions.move_to_element(element).click().perform()

    def scroll_to_element(self, element):
        """Scroll page smoothly until element is in the viewport center."""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.3)

    def scroll_into_view_by_locator(self, locator):
        """Scroll element identified by locator into view."""
        el = self.find_element(locator)
        self.scroll_to_element(el)
        return el

    def wait_for_url_contains(self, substring, timeout=None):
        """Wait until the current URL contains a given substring."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.url_contains(substring))

    def get_current_url(self):
        """Return the current page URL."""
        return self.driver.current_url

    def get_page_title(self):
        """Return current document title."""
        return self.driver.title

    def take_screenshot(self, name="screenshot"):
        """Save a timestamped screenshot to the reports directory."""
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOTS_DIR, filename)
        self.driver.save_screenshot(filepath)
        return filepath
