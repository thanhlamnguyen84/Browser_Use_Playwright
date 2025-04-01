from playwright.sync_api import Page, expect

def test_google_search(page: Page):
    # Navigate to Google
    page.goto("https://www.google.com")

    # Check that the page title contains "Google"
    expect(page).to_have_title("Google")

    # Locate the search input box
    search_box = page.locator("textarea[name='q']")
    search_box.fill("Playwright Python")

    # Press Enter to search
    search_box.press("Enter")

    # Wait for search results
    page.wait_for_selector("h3")

    # Assert that at least one search result is visible
    results = page.locator("h3")
    assert results.count() > 0, "No search results found!"  # ✅ Pass/Fail condition
