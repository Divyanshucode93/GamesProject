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

    def navigate(self, url, timeout=60000, wait_until='domcontentloaded'):
        """Navigates to the specified URL.
        
        Args:
            url: The URL to navigate to
            timeout: Maximum time in milliseconds to wait (default: 60000ms = 60s)
            wait_until: When to consider navigation successful. Options:
                - 'load': Wait for the load event
                - 'domcontentloaded': Wait for DOMContentLoaded event (faster, recommended for SPAs)
                - 'networkidle': Wait until no network connections for 500ms (slowest, may timeout on dynamic sites)
        """
        if not self.page:
            raise Exception("Browser not started. Call start() first.")
        print(f"Navigating to {url}...")
        self.page.goto(url, timeout=timeout, wait_until=wait_until)
        # Additional wait to ensure dynamic content loads
        print(f"Waiting for page to stabilize...")
        time.sleep(2)  # Give dynamic content time to render

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

    def get_html(self):
        """
        Returns the raw HTML content of the current page.
        """
        if not self.page:
            raise Exception("Browser not started.")
        return self.page.content()
    
    def save_html(self, filename):
        """
        Saves the current page's HTML content to a file.
        
        Args:
            filename: Path to save the HTML file
        """
        import os
        
        if not self.page:
            raise Exception("Browser not started.")
        
        html_content = self.page.content()
        
        # Ensure directory exists
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        # Save HTML to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML content saved to {filename}")
        print(f"File size: {len(html_content)} bytes")
        return filename
