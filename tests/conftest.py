"""
pytest conftest — fixtures for driver, parallel config, browser parametrization.
"""
import os
import pytest
import yaml

from utils.driver_factory import load_config, create_driver
from utils.logger import get_logger

CONFIG = load_config()
logger = get_logger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose test result for the driver fixture (used for screenshot on failure)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_addoption(parser):
    """Accept --lt flag for LambdaTest cloud execution."""
    parser.addoption(
        "--lt",
        action="store_true",
        default=False,
        help="Run on LambdaTest cloud instead of local browser",
    )


def pytest_generate_tests(metafunc):
    """Parametrize the 'browser' fixture from config.browsers."""
    if "browser" in metafunc.fixturenames:
        browsers = CONFIG.get("browsers", ["chrome"])
        metafunc.parametrize("browser", browsers, scope="function")


@pytest.fixture(scope="function")
def driver(request, browser):
    """Create a WebDriver (local or LambdaTest) per test."""
    use_lt = request.config.getoption("--lt")
    webdriver = create_driver(browser=browser.lower(), use_lambdatest=use_lt)
    webdriver.get(CONFIG["urls"]["amazon"])
    yield webdriver
    # Screenshot on failure for debugging
    if request.node.rep_call.failed:
        screenshot_path = f"screenshots/{request.node.name}_{browser}.png"
        os.makedirs("screenshots", exist_ok=True)
        webdriver.save_screenshot(screenshot_path)
        logger.info("📸 Screenshot saved: %s", screenshot_path)
    webdriver.quit()
