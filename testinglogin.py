# ================================
# FILE: utils/config.py
# ================================

BASE_URL = "https://www.saucedemo.com/"

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

INVALID_PASSWORD = "wrong_sauce"

WAIT_TIME = 10


# ================================
# FILE: utils/driver_factory.py
# ================================

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def initialize_browser():

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    logging.info("Chrome browser initialized.")

    return driver


def quit_browser(driver):

    if driver:
        driver.quit()
        logging.info("Browser closed successfully.")


# ================================
# FILE: pages/login_page.py
# ================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import WAIT_TIME


class LoginPage:

    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    INVENTORY_CONTAINER = (
        By.ID,
        "inventory_container"
    )

    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-test='error']"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            WAIT_TIME
        )

    def open_page(self, url):

        self.driver.get(url)

    def login(self, username, password):

        username_field = self.wait.until(
            ec.presence_of_element_located(
                self.USERNAME_FIELD
            )
        )

        password_field = self.wait.until(
            ec.presence_of_element_located(
                self.PASSWORD_FIELD
            )
        )

        login_button = self.wait.until(
            ec.element_to_be_clickable(
                self.LOGIN_BUTTON
            )
        )

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        login_button.click()

    def is_inventory_displayed(self):

        inventory = self.wait.until(
            ec.presence_of_element_located(
                self.INVENTORY_CONTAINER
            )
        )

        return inventory.is_displayed()

    def get_error_message(self):

        error = self.wait.until(
            ec.visibility_of_element_located(
                self.ERROR_MESSAGE
            )
        )

        return error.text


# ================================
# FILE: tests/test_login.py
# ================================

import logging

import pytest

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)

from pages.login_page import LoginPage

from utils.config import (
    BASE_URL,
    VALID_USERNAME,
    VALID_PASSWORD,
    INVALID_PASSWORD
)

from utils.driver_factory import (
    initialize_browser,
    quit_browser
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.fixture()
def driver():

    browser = initialize_browser()

    yield browser

    quit_browser(browser)


@pytest.mark.parametrize(
    "username,password,expected_result",
    [
        (
            VALID_USERNAME,
            VALID_PASSWORD,
            "success"
        ),
        (
            VALID_USERNAME,
            INVALID_PASSWORD,
            "failure"
        )
    ]
)
def test_login(
    driver,
    username,
    password,
    expected_result
):

    login_page = LoginPage(driver)

    try:

        login_page.open_page(BASE_URL)

        login_page.login(
            username=username,
            password=password
        )

        if expected_result == "success":

            assert (
                login_page.is_inventory_displayed()
            )

            logging.info(
                "TEST PASSED: Successful login."
            )

        else:

            error_message = (
                login_page.get_error_message()
            )

            assert "Epic sadface" in error_message

            logging.info(
                "TEST PASSED: Invalid login verified."
            )

    except TimeoutException:

        logging.error(
            "TEST FAILED: Timeout occurred."
        )

        raise

    except WebDriverException as error:

        logging.error(
            "TEST FAILED: WebDriver issue - %s",
            error
        )

        raise

    except Exception as error:

        logging.error(
            "TEST FAILED: Unexpected error - %s",
            error
        )

        raise


