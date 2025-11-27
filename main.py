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
        
        # Accept cookies if present
        scraper.accept_cookies()
        
        # Click on the PS5 element
        ps5_allpage1_games = "//h2[@id='title-b300e53a-d7d2-11ee-9d6a-d6ec549ae369']/following-sibling::div[@class='psw-preview-grid-list']//li" 

        # Scroll to the element to ensure it's in view
        scraper.scroll_to_element(ps5_allpage1_games)

        len_ps5_allpage1_games = scraper.get_element_count(ps5_allpage1_games)
        print(f"Number of PS5 games on page 1: {len_ps5_allpage1_games}")


        for i in range(len_ps5_allpage1_games):
            game_xpath = f"({ps5_allpage1_games})[{i + 1}]"
            print(f"Clicking on game {i + 1}...")
            scraper.click_element(game_xpath)
            scraper.wait_for_page_load()

            # TODO: Fetch specific web content from the game's detail page here
            # Example: Get the title of the game
            # game_title_xpath = "//h1[@data-qa='mfe-game-title#name']"
            # game_title = scraper.get_text(game_title_xpath)
            # print(f"  Game Title: {game_title}")

            scraper.go_back()
            scraper.wait_for_page_load()

        # scraper.click_element(ps5_allpage1_games)

        # Wait for the page to load
        scraper.wait_for_page_load()

        # # Save the raw HTML content to a file
        # html_file = "data/playstation_latest.html"
        # scraper.save_html(html_file)
        
        # print(f"\n✅ Page content saved successfully!")
        # print(f"📄 You can now process the HTML file: {html_file}")
        
        # Keep browser open for a moment to verify (optional)
        import time; time.sleep(3)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()