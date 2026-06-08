"""
Test Cases for Amazon iPhone and Galaxy search → add-to-cart flow.
Both tests run in parallel when executed with pytest-xdist -n2+.
"""
from pages.amazon_page import AmazonPage
from utils.driver_factory import load_config
from utils.logger import get_logger

logger = get_logger(__name__)
CONFIG = load_config()


def test_iphone_to_cart(driver, browser):
    """
    Test Case 1 — iPhone
    Search → open first result → add to cart → print price.
    """
    search_query = CONFIG["search"]["test1_query"]
    logger.info("═══ Test 1: Searching '%s' on %s ═══", search_query, browser)

    amazon = AmazonPage(driver)
    amazon.search(search_query)
    amazon.open_first_result()
    amazon.add_to_cart()
    price = amazon.get_price()

    logger.info("✅ Test 1 PASS — %s price: ₹%s", search_query, price)
    print(f"\n{'='*50}\niPhone price: ₹{price}\n{'='*50}")

    # Soft assertion — if price is empty, we still logged it
    assert bool(price), f"Price should not be empty for {search_query}"


def test_galaxy_to_cart(driver, browser):
    """
    Test Case 2 — Galaxy
    Search → open first result → add to cart → print price.
    """
    search_query = CONFIG["search"]["test2_query"]
    logger.info("═══ Test 2: Searching '%s' on %s ═══", search_query, browser)

    amazon = AmazonPage(driver)
    amazon.search(search_query)
    amazon.open_first_result()
    amazon.add_to_cart()
    price = amazon.get_price()

    logger.info("✅ Test 2 PASS — %s price: ₹%s", search_query, price)
    print(f"\n{'='*50}\nGalaxy price: ₹{price}\n{'='*50}")

    assert bool(price), f"Price should not be empty for {search_query}"
