"""
Amazon Page Object — search, add to cart, retrieve price.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class AmazonPage(BasePage):
    """Page Object for Amazon.in."""

    # ── Locators ──────────────────────────────────────
    SEARCH_BOX = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.ID, "nav-search-submit-button")
    # First organic result — Amazon can have sponsored blocks before it
    FIRST_RESULT = (By.CSS_SELECTOR, '[data-component-type="s-search-result"]:first-of-type h2 a')
    # Fallback: Amazon's own data-cel-widget attribute on search result rows
    FIRST_RESULT_FALLBACK = (By.CSS_SELECTOR, '[data-cel-widget*="search_result"]:first-of-type h2 a')
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button")
    CART_PRICE = (By.CSS_SELECTOR, ".a-price-whole")
    SIDEBAR_PRICE = (By.CSS_SELECTOR, "#attach-accessory-pane .a-price-whole")

    # ── Actions ───────────────────────────────────────

    def search(self, query: str) -> None:
        """Navigate to Amazon and search for a product."""
        logger.info("Searching Amazon for: %s", query)
        self.type(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)

    def open_first_result(self) -> None:
        """Click the first organic search result with fallback."""
        logger.info("Opening the first search result")
        # Try primary selector first
        if self.is_present(self.FIRST_RESULT, timeout=5):
            self.click(self.FIRST_RESULT)
        # Fallback to Amazon's data-cel-widget attribute
        elif self.is_present(self.FIRST_RESULT_FALLBACK, timeout=3):
            self.click(self.FIRST_RESULT_FALLBACK)
        # Last resort: any clickable link inside the search results
        else:
            logger.warning("Primary & fallback locators failed, trying generic first h2 a")
            self.click((By.CSS_SELECTOR, '[data-component-type="s-search-result"] h2 a:first-of-type'))

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
