"""
Base Page — common WebDriver operations for all page objects.
"""
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """Encapsulates reusable wait / click / type / scroll logic."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by: tuple) -> WebElement:
        """Wait for element to be present and return it."""
        return self.wait.until(EC.presence_of_element_located(by))

    def click(self, by: tuple) -> None:
        """Wait for element to be clickable, then click."""
        el = self.wait.until(EC.element_to_be_clickable(by))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        el.click()

    def type(self, by: tuple, text: str, clear_first: bool = True) -> None:
        """Type text into an input field."""
        el = self.find(by)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, by: tuple) -> str:
        """Return visible text of an element."""
        return self.find(by).text.strip()

    def is_present(self, by: tuple, timeout: int = 3) -> bool:
        """Check if element is present without raising."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(by))
            return True
        except TimeoutException:
            return False

    def current_url(self) -> str:
        return self.driver.current_url
