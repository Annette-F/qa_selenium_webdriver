from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_webdriver import shared
from selenium_webdriver.selector import to_locator


def element(selector):
    def find_visible(driver: WebDriver):
        webelement = driver.find_element(*to_locator(selector))
        if not webelement.is_displayed():
            raise AssertionError(f'element is not displayed: {webelement.get_attribute("outerHTML")}')
        return webelement

    return shared.wait.until(find_visible)


def type(selector, value):
    def command(driver: WebDriver) -> WebElement:
        webelement = driver.find_element(*to_locator(selector))
        webelement.send_keys(value)
        return webelement

    return shared.wait.until(command)


def click(selector):
    def command(driver: WebDriver) -> WebElement:
        webelement = driver.find_element(*to_locator(selector))
        webelement.click()
        return webelement

    return shared.wait.until(command)
