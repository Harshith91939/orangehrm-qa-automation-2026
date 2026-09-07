"""
Configuration settings for OrangeHRM Test Automation Suite
"""
import os

class Config:
    # Application URLs
    BASE_URL = os.getenv("ORANGEHRM_URL", "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    DASHBOARD_URL_SUBSTRING = "/dashboard/index"
    PIM_URL_SUBSTRING = "/pim/viewEmployeeList"
    ADD_EMP_URL_SUBSTRING = "/pim/addEmployee"
    
    # Credentials
    ADMIN_USERNAME = os.getenv("ORANGEHRM_USER", "Admin")
    ADMIN_PASSWORD = os.getenv("ORANGEHRM_PASS", "admin123")
    INVALID_USERNAME = "InvalidUser"
    INVALID_PASSWORD = "wrongpassword"
    
    # Timeouts
    EXPLICIT_WAIT = 15
    POLL_FREQUENCY = 0.5
    
    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
