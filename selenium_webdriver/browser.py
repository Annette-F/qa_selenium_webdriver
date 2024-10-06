from __future__ import annotations
from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_webdriver.conditions import that
from selenium_webdriver.selector import to_locator
from selenium_webdriver.wait import WebDriverWait
from dataclasses import dataclass


@dataclass
class Config:
    timeout: float = 2
    base_url: str = ''


class Element:
    def __init__(self, selector, browser: Browser):
        self.selector = selector
        self.browser = browser
        return self

    def type(self, value):
        self.browser.type(self.selector, value)
        return self

    def click(self):
        self.browser.click(self.selector)
        return self


class Collection:
    def __init__(self, selector, browser: Browser):
        self.selector = selector
        self.browser = browser
        return self

    def assert_amount(self, value):
        self.browser.assert_(that.number_of_elements(self.selector, value=value))
        return self


class Browser:
    def __init__(self, driver: WebDriver, config=Config()):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, timeout=config.timeout, ignored_exceptions=WebDriverException)
        return self

    def assert_(self, condition):
        return self.wait.until(condition)

    def open(self, relative_url):
        self.driver.get(self.config.base_url + relative_url)
        return self

    def back(self):
        self.driver.back()
        return self

    def quit(self):
        self.driver.quit()
        return self

    def type(self, selector, value):
        def command(driver: WebDriver) -> WebElement:
            webelement = driver.find_element(*to_locator(selector))
            webelement.send_keys(value)
            return webelement

        self.wait.until(command, message=f'failed to type «{value}» into element by {selector}')
        return self.element(selector)

    def click(self, selector):
        def command(driver: WebDriver) -> WebElement:
            webelement = driver.find_element(*to_locator(selector))
            webelement.click()
            return webelement

        self.wait.until(command, message=f'failed to click on element by {selector}')
        return self.element(selector)

    def element(self, selector) -> Element:
        return Element(selector, self)

    def all(self, selector) -> Collection:
        return Collection(selector, self)
