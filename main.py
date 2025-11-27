# scraper/main.py 
from scraper.base_scraper import BaseScraper

def main():
    # Initialize the scraper
    # Set headless=True for production/background scraping, False to see the browser
    scraper = BaseScraper(headless=False, slow_mo=1000)
    
    try:
        scraper.start()
        
        # Navigate to the target URL
        url = "https://store.playstation.com/en-in/pages/latest" 
        scraper.navigate(url)
        
        # Save the raw HTML content to a file
        html_file = "data/playstation_latest.html"
        scraper.save_html(html_file)
        
        print(f"\n✅ Page content saved successfully!")
        print(f"📄 You can now process the HTML file: {html_file}")
        
        # Keep browser open for a moment to verify (optional)
        import time; time.sleep(3)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()

# //h2[@id='title-b300e53a-d7d2-11ee-9d6a-d6ec549ae369']/following-sibling::div[@class='psw-preview-grid-list']//li