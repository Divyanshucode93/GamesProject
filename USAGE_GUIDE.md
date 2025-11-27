# PlayStation Store Scraper - Usage Guide

## Overview
This scraping framework fetches raw HTML content from web pages and saves it to files for later processing.

## Quick Start

### 1. Scrape a Page and Save HTML
```bash
python main.py
```

This will:
- Launch a browser (visible mode with slow motion for debugging)
- Navigate to the PlayStation Store latest games page
- Save the raw HTML to `data/playstation_latest.html`

### 2. Extract Data from Saved HTML
```bash
python extract_from_html.py
```

This demonstrates how to:
- Load the saved HTML file
- Extract data using BeautifulSoup
- Extract data using XPath queries
- Parse game information

## File Structure

```
GamesProject/
├── main.py                      # Main scraper script
├── extract_from_html.py         # HTML parsing examples
├── scraper/
│   ├── base_scraper.py          # Core scraping functionality
│   └── utils.py                 # Utility functions
└── data/
    └── playstation_latest.html  # Saved HTML content
```

## Key Features

### BaseScraper Class

#### Methods:
- `start()` - Initializes browser
- `navigate(url, timeout=60000, wait_until='domcontentloaded')` - Navigates to URL
- `save_html(filename)` - Saves current page HTML to file
- `get_html()` - Returns current page HTML as string
- `close()` - Closes browser

#### Configuration:
```python
scraper = BaseScraper(
    headless=False,  # Set True for background scraping
    slow_mo=1000     # Milliseconds delay between actions (for debugging)
)
```

### Navigation Options

The `navigate()` method supports different wait strategies:

```python
# Fast - waits for DOM to load (recommended for SPAs)
scraper.navigate(url, wait_until='domcontentloaded')

# Standard - waits for load event
scraper.navigate(url, wait_until='load')

# Slow - waits for network to be idle (may timeout on dynamic sites)
scraper.navigate(url, wait_until='networkidle')

# Custom timeout (in milliseconds)
scraper.navigate(url, timeout=90000)  # 90 seconds
```

## Extracting Data from HTML

### Method 1: BeautifulSoup (CSS Selectors)

```python
from bs4 import BeautifulSoup

html_content = load_html("data/playstation_latest.html")
soup = BeautifulSoup(html_content, 'html.parser')

# Find elements by class
games = soup.find_all('div', class_='game-card')

# Find elements by tag
titles = soup.find_all('h2')

# Navigate the DOM
for game in games:
    title = game.find('h2').text
    price = game.find('span', class_='price').text
```

### Method 2: XPath (Powerful Queries)

```python
from lxml import html

html_content = load_html("data/playstation_latest.html")
tree = html.fromstring(html_content)

# Extract with XPath
games = tree.xpath("//div[@class='game-card']")
titles = tree.xpath("//h2/text()")

# Complex XPath example from your code:
xpath = "//h2[@id='title-b300e53a-d7d2-11ee-9d6a-d6ec549ae369']/following-sibling::div[@class='psw-preview-grid-list']//li"
game_items = tree.xpath(xpath)
```

## Customization Examples

### Example 1: Scrape Multiple Pages

```python
from scraper.base_scraper import BaseScraper

scraper = BaseScraper(headless=True)
scraper.start()

urls = [
    "https://store.playstation.com/en-in/pages/latest",
    "https://store.playstation.com/en-in/pages/deals",
]

for i, url in enumerate(urls):
    scraper.navigate(url)
    scraper.save_html(f"data/page_{i}.html")

scraper.close()
```

### Example 2: Extract Specific Game Data

```python
from bs4 import BeautifulSoup
import pandas as pd

def extract_games(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    games = []
    # Update selectors based on actual HTML structure
    for game_card in soup.find_all('div', class_='game-card'):
        game = {
            'title': game_card.find('h3').text.strip(),
            'price': game_card.find('span', class_='price').text.strip(),
            'platform': game_card.find('span', class_='platform').text.strip(),
        }
        games.append(game)
    
    return pd.DataFrame(games)

# Usage
df = extract_games("data/playstation_latest.html")
df.to_csv("data/games.csv", index=False)
```

### Example 3: Wait for Specific Elements

```python
# In base_scraper.py, add a new method:
def wait_for_element(self, selector, timeout=30000):
    """Wait for an element to appear on the page."""
    self.page.wait_for_selector(selector, timeout=timeout)

# Usage in main.py:
scraper.navigate(url)
scraper.wait_for_element('.game-card', timeout=10000)
scraper.save_html("data/page.html")
```

## Troubleshooting

### Issue: Timeout Error
**Solution:** Increase timeout or change wait strategy:
```python
scraper.navigate(url, timeout=90000, wait_until='domcontentloaded')
```

### Issue: Empty or Incomplete HTML
**Solution:** Add explicit waits or increase slow_mo:
```python
scraper = BaseScraper(headless=False, slow_mo=2000)
# Or add sleep after navigation
import time
scraper.navigate(url)
time.sleep(5)  # Wait for dynamic content
scraper.save_html("data/page.html")
```

### Issue: Can't Find Elements
**Solution:** Inspect the HTML file to find correct selectors:
```bash
# View the HTML in browser
firefox data/playstation_latest.html

# Or search for specific text
grep -i "game" data/playstation_latest.html
```

## Tips

1. **Start with headless=False** to see what's happening
2. **Use slow_mo** during development to debug issues
3. **Inspect saved HTML** to find correct selectors
4. **Use browser DevTools** to test XPath/CSS selectors
5. **Handle dynamic content** with appropriate waits
6. **Save HTML first**, extract data later (separation of concerns)

## Next Steps

1. Inspect `data/playstation_latest.html` to understand the structure
2. Find the correct CSS selectors or XPath for game data
3. Update `extract_from_html.py` with your custom extraction logic
4. Save extracted data to CSV/JSON for analysis
