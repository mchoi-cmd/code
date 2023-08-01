"""
These tests cover DuckDuckGo searches.
"""

import pytest
from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_basic_duckduckgo_search_by_return(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for the phrase and click enter/return
    search_page.search_by_return(phrase)
    result_page.page_loaded()

    # THEN the search result query is the phrase
    assert phrase == result_page.search_input_value()

    # And the search result links pertain to the phrase
    titles = result_page.result_link_titles()
    matches = [t for t in titles if phrase.lower() in t.lower()]
    assert len(matches) > 0

    # And the search result title contains the phrase
    assert phrase in result_page.title()


@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_basic_duckduckgo_search_by_button(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user searches for the phrase and click submit button
    search_page.search_by_button(phrase)
    result_page.page_loaded()

    # THEN the search result query is the phrase
    assert phrase == result_page.search_input_value()

    # And the search result links pertain to the phrase
    titles = result_page.result_link_titles()
    matches = [t for t in titles if phrase.lower() in t.lower()]
    assert len(matches) > 0

    # And the search result title contains the phrase
    assert phrase in result_page.title()

@pytest.mark.parametrize("phrase", ["panda"])
def test_basic_duckduckgo_click_on_a_result(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    # and the user searches for the phrase
    # and the results is loaded
    search_page.load()
    search_page.search_by_button(phrase)
    result_page.page_loaded()

    # When the user click on the first result
    links = result_page.result_links()
    titles = result_page.result_link_titles()
    links[0].click()

    # Then the link will display
    assert titles[0] == browser.title




# Independent Excercies (TODO)
# expand "More Results" at the bottom of the result page
# verify auto-complete suggestions pertain to the search text
# search by selecting an auto-complete suggestion
# search a new phrase from the results page
# do an image search
# do a video search
# do a news search
# change settings
# change region