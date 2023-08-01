"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo search result page.
"""

import time
from selenium.webdriver.common.by import By


class DuckDuckGoResultPage:

    # Locators
    RESULT_LINKS = (By.XPATH, "//a[@data-testid='result-title-a']")
    SEARCH_INPUT = (By.ID, "search_form_input")
    DUCK_BAR = (By.ID, "duckbar")

    # Initializer
    def __init__(self, browser):
      self.browser = browser

    # Interaction Methods
    def page_loaded(self): # Safari only - NoSuchFrameException error if this is not used
      if self.browser.capabilities["browserName"] == "Safari":
        time.sleep(1)

    def result_link_titles(self):
      links = self.result_links()
      titles = [link.text for link in links]
      return titles

    def result_links(self):
      links = self.browser.find_elements(*self.RESULT_LINKS)
      return links

    def search_input_value(self):
      search_input = self.browser.find_element(*self.SEARCH_INPUT)
      value = search_input.get_attribute('value')
      return value

    def title(self):
      return self.browser.title
