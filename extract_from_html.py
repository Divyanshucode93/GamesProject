"""
Helper script to extract data from saved HTML files.
This script demonstrates how to parse the saved HTML and extract game data.
"""

from bs4 import BeautifulSoup
from lxml import html
import json

def load_html(filename):
    """Load HTML content from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def extract_with_beautifulsoup(html_content):
    """
    Example: Extract data using BeautifulSoup.
    Modify this function based on what you want to extract.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Example: Extract page title
    title = soup.title.string if soup.title else "No title"
    
    # Example: Find all links
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    
    return {
        'title': title,
        'total_links': len(links),
        'sample_links': links[:5]  # First 5 links
    }

def extract_with_xpath(html_content, xpath_query):
    """
    Extract data using XPath.
    
    Args:
        html_content: The HTML string
        xpath_query: XPath expression to extract data
        
    Example XPath from your main.py:
        //h2[@id='title-b300e53a-d7d2-11ee-9d6a-d6ec549ae369']/following-sibling::div[@class='psw-preview-grid-list']//li
    """
    tree = html.fromstring(html_content)
    elements = tree.xpath(xpath_query)
    
    results = []
    for element in elements:
        # Check if element is a string (text node) or an Element
        if isinstance(element, str):
            results.append(element.strip())
        else:
            # Extract text content from element
            text = element.text_content().strip()
            results.append(text)
    
    return results

def extract_games_data(html_content):
    """
    Custom function to extract PlayStation games data.
    Modify this based on the actual structure of the page.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    games = []
    
    # Example: Find game cards (you'll need to inspect the HTML to find the right selectors)
    # This is a placeholder - update with actual selectors
    game_elements = soup.find_all('li', class_='psw-l-grid-item')
    
    for game in game_elements:
        game_data = {
            'title': game.get_text(strip=True),
            # Add more fields as needed
        }
        games.append(game_data)
    
    return games

def main():
    """Main function to demonstrate usage."""
    
    # Load the saved HTML
    html_file = "data/playstation_latest.html"
    print(f"Loading HTML from {html_file}...")
    html_content = load_html(html_file)
    print(f"✅ Loaded {len(html_content)} bytes of HTML content\n")
    
    # Example 1: Extract basic info with BeautifulSoup
    print("=" * 60)
    print("Example 1: Basic extraction with BeautifulSoup")
    print("=" * 60)
    basic_info = extract_with_beautifulsoup(html_content)
    print(json.dumps(basic_info, indent=2))
    
    # Example 2: Extract with XPath
    print("\n" + "=" * 60)
    print("Example 2: Extract with XPath")
    print("=" * 60)
    # Update this XPath based on what you want to extract
    xpath_query = "//title/text()"
    xpath_results = extract_with_xpath(html_content, xpath_query)
    print(f"XPath results: {xpath_results}")
    
    # Example 3: Custom game extraction
    print("\n" + "=" * 60)
    print("Example 3: Extract games data")
    print("=" * 60)
    games = extract_games_data(html_content)
    print(f"Found {len(games)} games")
    if games:
        print(f"Sample game: {games[0]}")

if __name__ == "__main__":
    main()
