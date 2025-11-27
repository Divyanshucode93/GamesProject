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
        # Create page with maximized viewport
        self.page = self.browser.new_page(viewport={'width': 1920, 'height': 1080})
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

    def click_element(self, selector):
        """Clicks an element on the page."""
        if not self.page:
            raise Exception("Browser not started.")
        self.page.click(selector)

    def go_back(self):
        """Navigates back to the previous page."""
        if not self.page:
            raise Exception("Browser not started.")
        
        try:
            # go_back() returns a Response object or None
            response = self.page.go_back(timeout=30000)  # 30 second timeout
            
            # Try to wait for page to be fully loaded, but don't fail if it times out
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                time.sleep(1)  # Small additional wait
            except:
                # Page might still be loading, but we can proceed
                print("Note: Page still loading after going back, continuing anyway...")
            
            return response
        except Exception as e:
            raise Exception(f"Failed to navigate back: {str(e)}")

    def get_element_count(self, selector):
        """
        Returns the count of elements matching the given selector.
        
        Args:
            selector: CSS selector or XPath to count elements
            
        Returns:
            int: Number of elements found
        """
        if not self.page:
            raise Exception("Browser not started.")
        
        # Wait for at least one element to appear (with timeout)
        try:
            self.page.wait_for_selector(selector, timeout=10000)
        except:
            # If no elements found, return 0
            return 0
        
        # Count all matching elements
        elements = self.page.locator(selector)
        return elements.count()
    
    def wait_for_page_load(self, timeout=30000):
        """
        Waits for the page to be fully loaded.
        
        Args:
            timeout: Maximum time in milliseconds to wait (default: 30000ms = 30s)
        """
        if not self.page:
            raise Exception("Browser not started.")
        
        try:
            # Wait for DOM content to be loaded (more reliable than networkidle)
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            # Additional small wait for dynamic content
            time.sleep(1)
        except Exception as e:
            print(f"Warning: Page load wait timed out: {e}")
    
    def get_text(self, selector):
        """
        Gets the text content of an element.
        
        Args:
            selector: CSS selector or XPath of the element
            
        Returns:
            str: Text content of the element
        """
        if not self.page:
            raise Exception("Browser not started.")
        
        try:
            element = self.page.locator(selector)
            return element.text_content()
        except Exception as e:
            raise Exception(f"Failed to get text from selector '{selector}': {str(e)}")

    def accept_cookies(self, timeout=10000):
        """
        Attempts to accept cookies by clicking common cookie consent buttons.
        
        Args:
            timeout: Maximum time in milliseconds to wait for cookie button
        """
        if not self.page:
            raise Exception("Browser not started.")
        
        # Common selectors for cookie accept buttons
        cookie_selectors = [
            "button:has-text('Accept')",
            "button:has-text('Accept All')",
            "button:has-text('I Accept')",
            "button:has-text('Agree')",
            "[data-qa='accept-cookies']",
            "#onetrust-accept-btn-handler",
            ".cookie-accept",
            "button[id*='accept']",
            "button[class*='accept']"
        ]
        
        for selector in cookie_selectors:
            try:
                # Wait for the button to appear
                self.page.wait_for_selector(selector, timeout=timeout, state='visible')
                print(f"Found cookie button with selector: {selector}")
                # Click the button
                self.page.click(selector)
                print("✅ Cookies accepted!")
                time.sleep(1)  # Wait for cookie banner to disappear
                return True
            except:
                continue
        
        print("ℹ️  No cookie consent button found (or already accepted)")
        return False
    
    def scroll_to_element(self, selector, timeout=10000):
        """
        Scrolls to an element to bring it into view.
        
        Args:
            selector: CSS selector or XPath of the element to scroll to
            timeout: Maximum time in milliseconds to wait for element
        """
        if not self.page:
            raise Exception("Browser not started.")
        
        try:
            # Wait for element to exist
            self.page.wait_for_selector(selector, timeout=timeout)
            # Scroll element into view
            self.page.locator(selector).first.scroll_into_view_if_needed()
            print(f"Scrolled to element: {selector}")
            time.sleep(0.5)  # Small wait after scrolling
            return True
        except Exception as e:
            print(f"Warning: Could not scroll to element '{selector}': {e}")
            return False

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
