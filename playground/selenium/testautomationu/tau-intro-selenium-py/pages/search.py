"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class DuckDuckGoSearchPage:

    # URL
    URL = "https://www.duckduckgo.com"

    # Locators
    SEARCH_INPUT = (By.ID, "searchbox_input")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Initializer
    def __init__(self, browser):
      self.browser = browser

    # Interaction Methods
    def load(self):
      self.browser.get(self.URL)

    def search_by_return(self, phrase):
      search_input = self.browser.find_element(*self.SEARCH_INPUT)
      search_input.send_keys(phrase + Keys.RETURN)

    def search_by_button(self, phrase):
      search_input = self.browser.find_element(*self.SEARCH_INPUT)
      search_input.send_keys(phrase)
      submit_button = self.browser.find_element(*self.SUBMIT_BUTTON)
      submit_button.click()