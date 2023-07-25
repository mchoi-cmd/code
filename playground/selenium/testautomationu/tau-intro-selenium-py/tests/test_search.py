"""
These tests cover DuckDuckGo searches.
"""

import pytest

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage

@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_basic_duckduckgo_search(browser, phrase):
  search_page = DuckDuckGoSearchPage(browser)
  result_page = DuckDuckGoResultPage(browser)

  # Given the DuckDuckGo home page is displayed
  search_page.load()

  # When the user searches for the phrase
  search_page.search(phrase)
  result_page.page_loaded()

  # THEN the search result query is the phrase
  assert phrase == result_page.search_input_value()

  # And the search result links pertain to the phrase
  titles = result_page.result_link_titles()
  matches = [t for t in titles if phrase.lower() in t.lower()]
  assert len(matches) > 0

  # And the search result title contains the phrase
  assert phrase in result_page.title()


# Independent Excercies (TODO)
# search for different phrases
# search by clicking the button instead of typing RETURN
# click a search result
# expand "More Results" at the bottom of the result page
# verify auto-complete suggestions pertain to the search text
# search by selecting an auto-complete suggestion
# search a new phrase from the results page
# do an image search
# do a video search
# do a news search
# change settings
# change region