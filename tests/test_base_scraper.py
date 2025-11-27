import pytest
from unittest.mock import MagicMock, patch
from scraper.base_scraper import BaseScraper

@pytest.fixture
def scraper():
    return BaseScraper(headless=True)

def test_init(scraper):
    assert scraper.headless is True
    assert scraper.playwright is None
    assert scraper.browser is None
    assert scraper.page is None

@patch('scraper.base_scraper.sync_playwright')
def test_start(mock_sync_playwright, scraper):
    mock_playwright_instance = MagicMock()
    mock_browser = MagicMock()
    mock_page = MagicMock()
    
    mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
    mock_playwright_instance.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page
    
    scraper.start()
    
    assert scraper.playwright == mock_playwright_instance
    assert scraper.browser == mock_browser
    assert scraper.page == mock_page
    mock_playwright_instance.chromium.launch.assert_called_once_with(headless=True)
    mock_browser.new_page.assert_called_once()

def test_navigate(scraper):
    scraper.page = MagicMock()
    url = "https://example.com"
    scraper.navigate(url)
    scraper.page.goto.assert_called_once_with(url)
    scraper.page.wait_for_load_state.assert_called_once_with('networkidle')

def test_navigate_no_browser(scraper):
    with pytest.raises(Exception, match="Browser not started"):
        scraper.navigate("https://example.com")

def test_get_content(scraper):
    scraper.page = MagicMock()
    scraper.page.content.return_value = "<html></html>"
    content = scraper.get_content()
    assert content == "<html></html>"

def test_get_content_no_browser(scraper):
    with pytest.raises(Exception, match="Browser not started"):
        scraper.get_content()

def test_close(scraper):
    scraper.browser = MagicMock()
    scraper.playwright = MagicMock()
    
    scraper.close()
    
    scraper.browser.close.assert_called_once()
    scraper.playwright.stop.assert_called_once()
