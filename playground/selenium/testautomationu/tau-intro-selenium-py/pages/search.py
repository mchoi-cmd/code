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
    SUGGESTIONS = (By.XPATH, "//li[@role='option']")

    # Initializer
    def __init__(self, browser):
        self.browser = browser

    # Interaction Methods
    def load(self):
        self.browser.get(self.URL)

    def search_by_return(self, phrase):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase + Keys.RETURN)

    def type_in_search_box(self, phrase):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase)

    def click_submit_button(self):
        submit_button = self.browser.find_element(*self.SUBMIT_BUTTON)
        submit_button.click()

    def auto_complete_suggestions(self):
        suggestions = self.browser.find_elements(*self.SUGGESTIONS)
        suggestion_phrases = [suggestion.accessible_name for suggestion in suggestions]
        return suggestion_phrases

    # Complex interaction methods
    def load_duckduckgo_and_search_phrase_by_button(self, phrase):
        self.load()
        self.search_by_button(phrase)

    def search_by_button(self, phrase):
        self.type_in_search_box(phrase)
        self.click_submit_button()
