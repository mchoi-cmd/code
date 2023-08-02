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
    # And the search result links pertain to the phrase
    # And the search result title contains the phrase
    verify_basic_duckduckgo_result_page(result_page, phrase)


@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_basic_duckduckgo_search_by_button(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    # When the user searches for the phrase and click submit button
    search_page.load_duckduckgo_and_search_phrase_by_button(phrase)

    # THEN the search result query is the phrase
    # And the search result links pertain to the phrase
    # And the search result title contains the phrase
    verify_basic_duckduckgo_result_page(result_page, phrase)


@pytest.mark.parametrize("phrase", ["panda"])
def test_basic_duckduckgo_click_on_a_result(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    # and the user searches for the phrase
    # and the results is loaded
    search_page.load_duckduckgo_and_search_phrase_by_button(phrase)

    # When the user click on the first result
    links = result_page.result_links()
    titles = result_page.result_link_titles()
    links[0].click()

    # Then the link will display
    assert titles[0] == browser.title


@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_duckduckgo_expand_more_results(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)
    result_page = DuckDuckGoResultPage(browser)

    # Given the DuckDuckGo home page is displayed
    # And the user searches for the phrase
    # And the result page is displayed

    search_page.load_duckduckgo_and_search_phrase_by_button(phrase)
    result_page.page_loaded()
    matches_before = result_page.number_of_matched_results(phrase)

    # When the user click on more results button
    result_page.more_results_button().click()
    matches_after = result_page.number_of_matched_results(phrase)

    # THEN the number of matches will increase
    assert matches_before < matches_after


@pytest.mark.parametrize("phrase", ["panda", "python", "polar bear"])
def test_duckduckgo_auto_complete_suggestions(browser, phrase):
    search_page = DuckDuckGoSearchPage(browser)

    # Given the DuckDuckGo home page is displayed
    search_page.load()

    # When the user type a phrase in search box
    search_page.type_in_search_box(phrase)
    search_page.type_in_search_box(" ")
    suggestions = search_page.auto_complete_suggestions()
    num_suggestions = len(suggestions)

    # Then auto complete suggestions should appear
    assert num_suggestions > 0
    # And auto complete suggestions contain the original phrase
    matches = [t for t in suggestions if phrase.lower() in t.lower()]

    assert num_suggestions == len(matches)


# Helper methods
def verify_basic_duckduckgo_result_page(result_page, phrase):
    result_page.page_loaded()

    # THEN the search result query is the phrase
    assert phrase == result_page.search_input_value()

    # And the search result links pertain to the phrase
    assert result_page.number_of_matched_results(phrase) > 0

    # And the search result title contains the phrase
    assert phrase in result_page.title()


# Independent Excercies (TODO)
# verify auto-complete suggestions pertain to the search text
# search by selecting an auto-complete suggestion
# search a new phrase from the results page
# do an image search
# do a video search
# do a news search
# change settings
# change region
