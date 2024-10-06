from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_webdriver.selector import to_locator
from selenium_webdriver.wait import WebDriverWait

driver: WebDriver = ...
wait: WebDriverWait = ...


def assert_(condition):
    return wait.until(condition)


def open(url):
    driver.get(url)


def back():
    driver.back()


def quit():
    driver.quit()


def element(selector):
    def find_visible(driver: WebDriver):
        webelement = driver.find_element(*to_locator(selector))
        if not webelement.is_displayed():
            raise AssertionError(f'element is not displayed: {webelement.get_attribute("outerHTML")}')
        return webelement

    return wait.until(find_visible, message=f'element by {selector} is not ready')


def type(selector, value):
    def command(driver: WebDriver) -> WebElement:
        webelement = driver.find_element(*to_locator(selector))
        webelement.send_keys(value)
        return webelement

    return wait.until(command, message=f'failed to type «{value}» into element by {selector}')


def click(selector):
    def command(driver: WebDriver) -> WebElement:
        webelement = driver.find_element(*to_locator(selector))
        webelement.click()
        return webelement

    return wait.until(command, message=f'failed to click on element by {selector}')
