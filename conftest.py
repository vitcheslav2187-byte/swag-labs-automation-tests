import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

@pytest.fixture(scope="function")
def driver():
    """Initialize WebDriver with error handling for browser version detection"""
    chrome_options = Options()
    
    if HEADLESS:
        chrome_options.add_argument("--headless")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # Fallback: Use Chrome with system PATH if WebDriver Manager fails
        print(f"WebDriver Manager error: {e}")
        print("Attempting to use system Chrome...")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            print(f"Failed to initialize Chrome: {e2}")
            pytest.skip(f"Chrome browser not available: {e2}")
    
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    
    yield driver
    driver.quit()
