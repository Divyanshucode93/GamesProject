import pytest
from unittest.mock import patch
from main import main

@patch('main.BaseScraper')
def test_main(mock_base_scraper):
    mock_scraper_instance = mock_base_scraper.return_value
    
    main()
    
    mock_base_scraper.assert_called_once_with(headless=False)
    mock_scraper_instance.start.assert_called_once()
    mock_scraper_instance.close.assert_called_once()
