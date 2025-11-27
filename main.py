# scraper/main.py 
from scraper.base_scraper import BaseScraper
from scraper.utils import save_to_csv

def main():
    # Initialize the scraper
    # Set headless=True for production/background scraping, False to see the browser
    scraper = BaseScraper(headless=False, slow_mo=1000)
    
    try:
        scraper.start()
        
        # Example usage:
        # url = "https://example.com" 
        url = "https://store.playstation.com/en-in/pages/latest" 
        scraper.navigate(url)
        data = scraper.extract_data()
        save_to_csv(data, "data/output.csv")
        
        print("Framework initialized successfully. Ready to scrape!")
        
        # Keep browser open for a moment to verify (optional)
        import time; time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()

# //h2[@id='title-b300e53a-d7d2-11ee-9d6a-d6ec549ae369']/following-sibling::div[@class='psw-preview-grid-list']//li