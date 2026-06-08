"""
Amazon Page Object — search, add to cart, retrieve price.
"""
import os
import time
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.driver_factory import load_config
from utils.logger import get_logger

logger = get_logger(__name__)
CONFIG = load_config()


class AmazonPage(BasePage):
    """Page Object for Amazon.in."""

    # ── Locators ──────────────────────────────────────
    # Use direct URL navigation instead of search box (avoids headless detection)
    PRODUCT_LINK = (By.CSS_SELECTOR, 'div[data-component-type="s-search-result"]:first-of-type h2 a')
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button")
    ADD_TO_CART_FALLBACK = (By.NAME, "submit.add-to-cart")
    CART_PRICE = (By.CSS_SELECTOR, ".a-price-whole")
    SIDEBAR_PRICE = (By.CSS_SELECTOR, "#attach-accessory-pane .a-price-whole")

    # ── Actions ───────────────────────────────────────

    def search(self, query: str) -> None:
        """Navigate directly to search results page (bypasses search box)."""
        url = f"{CONFIG['urls']['amazon']}/s?k={query.replace(' ', '+')}"
        logger.info("Navigating to: %s", url)
        self.driver.get(url)

    def open_first_result(self) -> None:
        """Click the first organic search result."""
        logger.info("Opening the first search result")
        if self.is_present(self.PRODUCT_LINK, timeout=10):
            self.click(self.PRODUCT_LINK)
        else:
            # Dump page source for debugging
            os.makedirs("debug", exist_ok=True)
            with open(f"debug/page_dump_{int(time.time())}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            logger.error("First product link not found. Page title: %s", self.driver.title)
            raise RuntimeError(f"Could not find any product link on search results. Page title: {self.driver.title}")

    def add_to_cart(self) -> None:
        """Click 'Add to Cart'."""
        logger.info("Adding item to cart")
        self.click(self.ADD_TO_CART_BUTTON)

    def get_price(self) -> str:
        """Retrieve the displayed price from cart sidebar or main area."""
        if self.is_present(self.SIDEBAR_PRICE, timeout=4):
            price = self.get_text(self.SIDEBAR_PRICE)
        else:
            price = self.get_text(self.CART_PRICE)
        logger.info("Price found: ₹%s", price)
        return price
