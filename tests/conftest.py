"""
Pytest configuration, fixtures, and hooks for OrangeHRM test suite.
"""
import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config.config import Config


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run browser in headless mode: true or false"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Target browser: chrome or edge"
    )


@pytest.fixture(scope="function")
def driver(request):
    """WebDriver fixture managing browser lifecycle with auto-teardown and failure screenshot."""
    headless_opt = request.config.getoption("--headless").lower() in ("true", "1", "yes")
    browser_opt = request.config.getoption("--browser").lower()

    if browser_opt == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        if headless_opt:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
        web_driver = webdriver.Edge(options=options)
    else:
        options = ChromeOptions()
        if headless_opt:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        web_driver = webdriver.Chrome(options=options)

    web_driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    yield web_driver

    # Capture failure screenshot if needed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        test_name = request.node.name
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        ss_path = os.path.join(Config.SCREENSHOTS_DIR, f"FAIL_{test_name}_{ts}.png")
        try:
            web_driver.save_screenshot(ss_path)
            print(f"\n[FAILURE SCREENSHOT SAVED]: {ss_path}")
        except Exception:
            pass

    web_driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to attach test execution status to node for fixture inspection."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "OrangeHRM QA Automation Execution Report"
