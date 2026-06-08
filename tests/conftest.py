"""
pytest conftest — fixtures for driver, parallel config, browser parametrization.
"""
import os
import pytest
import yaml

from utils.driver_factory import load_config, create_driver

CONFIG = load_config()


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
    webdriver.quit()
