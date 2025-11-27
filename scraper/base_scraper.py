from playwright.sync_api import sync_playwright
import time

class BaseScraper:
    def __init__(self, headless=False, slow_mo=0):
        self.headless = headless
        self.slow_mo = slow_mo
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        """Starts the Playwright engine and browser."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless, slow_mo=self.slow_mo)
        self.page = self.browser.new_page()
        print("Browser started.")

    def navigate(self, url):
        """Navigates to the specified URL."""
        if not self.page:
            raise Exception("Browser not started. Call start() first.")
        print(f"Navigating to {url}...")
        self.page.goto(url)
        # Wait for load state to ensure page is ready
        self.page.wait_for_load_state('networkidle')

    def get_content(self):
        """Returns the HTML content of the current page."""
        if not self.page:
            raise Exception("Browser not started.")
        return self.page.content()

    def close(self):
        """Closes the browser and stops Playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("Browser closed.")

    def extract_data(self):
        """
        Placeholder for data extraction logic.
        Override this method in subclasses or implement specific logic here.
        """
        print("Extracting data... (Implement logic here)")
        html_content = self.page.content()
        print("Data extraction complete...")
        return html_content
