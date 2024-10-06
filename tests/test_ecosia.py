from selenium.webdriver import Keys

from tests import web
from tests.web import browser

browser.open('/')

web.ecosia.query.type('selene' + Keys.ENTER)

browser.back()

web.ecosia.query.type(' github issues' + Keys.ENTER)

web.ecosia.first_result_link.click()
web.github_issues.links.assert_amount(24)

browser.quit()
