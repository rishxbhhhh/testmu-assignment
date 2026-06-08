"""
Driver Factory — creates local (Chrome/Edge) or LambdaTest remote WebDriver.
"""
import os
import json
from datetime import datetime
from typing import Optional

import yaml
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from utils.logger import get_logger

logger = get_logger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")


def load_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def _chrome_options() -> webdriver.ChromeOptions:
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1366,768")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    return opts


def _edge_options() -> webdriver.EdgeOptions:
    opts = webdriver.EdgeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1366,768")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    return opts


def build_local_driver(browser: str = "chrome") -> WebDriver:
    """Create a local WebDriver for the given browser."""
    browser = browser.lower()
    if browser == "chrome":
        driver = webdriver.Chrome(options=_chrome_options())
    elif browser == "edge":
        driver = webdriver.Edge(options=_edge_options())
    else:
        raise ValueError(f"Unsupported local browser: {browser}")

    config = load_config()
    driver.implicitly_wait(config.get("default_wait", 10))
    logger.info("Local %s driver started", browser)
    return driver


def build_lt_driver(browser_cfg: dict) -> WebDriver:
    """Create a remote WebDriver pointed at LambdaTest cloud."""
    username = os.getenv("LT_USERNAME")
    access_key = os.getenv("LT_ACCESS_KEY")
    if not username or not access_key:
        raise RuntimeError("Set LT_USERNAME and LT_ACCESS_KEY env vars for LambdaTest.")

    config = load_config()
    lt = config.get("lambdatest", {})
    build_name = lt.get("build_name", "TestMu Assignment").format(datetime=datetime.now().isoformat())

    lt_options = {
        "user": username,
        "accessKey": access_key,
        "build": build_name,
        "name": f"{browser_cfg['browser']} — {browser_cfg.get('version', 'latest')}",
        "platformName": browser_cfg.get("platform", "Windows 11"),
        "w3c": True,
        "browserName": browser_cfg["browser"],
        "browserVersion": browser_cfg.get("version", "latest"),
        "selenoid:options": {"enableVNC": True, "enableVideo": False},
    }

    options = webdriver.ChromeOptions()
    options.set_capability("LT:Options", lt_options)

    driver = webdriver.Remote(
        command_executor=lt.get("hub_url", "https://hub.lambdatest.com/wd/hub"),
        options=options,
    )
    driver.implicitly_wait(config.get("default_wait", 10))
    logger.info("LambdaTest driver started: %s", browser_cfg["browser"])
    return driver


def create_driver(browser: str = "chrome", use_lambdatest: bool = False) -> WebDriver:
    """Factory entry: returns a driver (local or LambdaTest)."""
    if use_lambdatest:
        config = load_config()
        lt_cfgs = config.get("lambdatest", {}).get("browsers", [])
        matched = [c for c in lt_cfgs if c["browser"].lower() == browser.lower()]
        if not matched:
            raise ValueError(f"Browser '{browser}' not in lambdatest.browsers config")
        return build_lt_driver(matched[0])
    return build_local_driver(browser)
