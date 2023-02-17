# Copyright Michael Choi All Rights Reserved

import re
from playwright.sync_api import Page, expect, sync_playwright



def test(page: Page):
    pw = sync_playwright()
    pw.c
    browser = chromium.launch()    
    context = browser.new_context()
    
    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://subsplease.org/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("SubsPlease"))

    # create a locator
    shows = page.get_by_role("link", name="Shows")

    # Expect an attribute "to be strictly equal" to the value.
    expect(shows).to_have_attribute("href", "https://subsplease.org/shows/")

    # # Click the get started link.
    shows.click()

    # # Expects the URL to contain intro.
    expect(page.get_by_role("heading", name="*SubsPlease*"))

    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path = "trace.zip")


# with sync_playwright() as playwright:
#     run(playwright) 