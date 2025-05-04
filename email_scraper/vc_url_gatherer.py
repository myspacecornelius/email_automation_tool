import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import json
import time
import csv
import logging
import os
import random
from typing import Set
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vc_url_gatherer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VCUrlGatherer:
    def __init__(self, output_file='email_scraper/vc_firms_urls.csv'):
        self.output_file = output_file
        self.checkpoint_file = f"{output_file}.checkpoint"
        self.ua = UserAgent()
        self.urls: Set[str] = self.load_checkpoint()
        self.session = self.setup_session()
        self.driver = self.setup_driver()
        self.last_request_time = 0
        self.min_request_interval = 2  # seconds

    def setup_session(self) -> requests.Session:
        """Setup requests session with retry mechanism"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        return session

    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome WebDriver with proper error handling"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument(f'user-agent={self.ua.random}')
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            
            return webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def load_checkpoint(self) -> Set[str]:
        """Load URLs from checkpoint file if it exists"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except Exception as e:
                logger.error(f"Error loading checkpoint: {e}")
        return set()

    def save_checkpoint(self) -> None:
        """Save current URLs to checkpoint file"""
        try:
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.urls), f)
            logger.info(f"Saved checkpoint with {len(self.urls)} URLs")
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")

    def rate_limit(self) -> None:
        """Ensure minimum time between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def gather_urls(self) -> None:
        """Gather URLs from multiple sources"""
        try:
            self.gather_from_vc_directories()
            self.gather_from_search_engines()
            self.save_urls()
        except Exception as e:
            logger.error(f"Error during URL gathering: {e}")
            self.save_checkpoint()  # Save progress even if there's an error
        finally:
            self.driver.quit()

    def gather_from_vc_directories(self) -> None:
        """Gather URLs from known VC directories"""
        directories = [
            # [Previous extensive list of directories remains the same]
            # Major Global VC Directories
            'https://www.crunchbase.com/hub/venture-capital-firms',
            'https://www.vcaonline.com/firms/',
            'https://airtable.com/shrkohpeE2AO2ldeq/tbl5Q8N7NuW22z5Bt?backgroundColor=cyan&viewControls=on',
            'https://mercury.com/investor-db',
            'https://docs.google.com/spreadsheets',
            'https://airtable.com/shrWa2dHIwRjTTKwF',
            
            
            # ... [rest of the directories list]
        ]

        for directory in directories:
            try:
                logger.info(f"Gathering URLs from {directory}")
                self.rate_limit()
                
                # Retry mechanism
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.driver.get(directory)
                        break
                    except Exception as e:
                        if attempt == max_retries - 1:
                            raise
                        logger.warning(f"Retry {attempt + 1} for {directory}: {e}")
                        time.sleep(random.uniform(2, 5))
                
                # Wait for dynamic content and scroll
                self.scroll_page()
                
                # Find and collect VC firm URLs
                links = self.driver.find_elements(By.TAG_NAME, "a")
                new_urls = 0
                for link in links:
                    url = link.get_attribute('href')
                    if url and self.is_vc_firm_url(url):
                        if url not in self.urls:
                            self.urls.add(url)
                            new_urls += 1
                            logger.debug(f"Found new VC firm URL: {url}")
                
                if new_urls > 0:
                    logger.info(f"Found {new_urls} new URLs from {directory}")
                    self.save_checkpoint()

            except Exception as e:
                logger.error(f"Error gathering from {directory}: {e}")

    def scroll_page(self) -> None:
        """Scroll page to load dynamic content"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1.0, 2.0))
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logger.error(f"Error scrolling page: {e}")

    def gather_from_search_engines(self) -> None:
        """Gather URLs using search engines with rate limiting"""
        search_queries = [
            "top venture capital firms",
            "VC firms contact",
            # ... [previous search queries remain the same]
        ]

        for query in search_queries:
            try:
                logger.info(f"Searching for: {query}")
                self.rate_limit()
                
                url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                new_urls = 0
                
                for link in soup.find_all('a'):
                    url = link.get('href')
                    if url and self.is_vc_firm_url(url) and url not in self.urls:
                        self.urls.add(url)
                        new_urls += 1
                        logger.debug(f"Found new VC firm URL from search: {url}")
                
                if new_urls > 0:
                    logger.info(f"Found {new_urls} new URLs from search query: {query}")
                    self.save_checkpoint()
                
                # Random delay between searches
                time.sleep(random.uniform(2.0, 4.0))
                
            except Exception as e:
                logger.error(f"Error gathering from search for query '{query}': {e}")

    def is_vc_firm_url(self, url: str) -> bool:
        """Check if URL likely belongs to a VC firm"""
        if not url:
            return False
            
        url_lower = url.lower()
        
        # Skip social media and generic sites
        skip_domains = [
            'linkedin.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'medium.com', 'wikipedia.org', 'crunchbase.com',
            'bloomberg.com', 'reuters.com', 'wsj.com', 'forbes.com',
            'techcrunch.com', 'slideshare.net', 'github.com'
        ]
        
        if any(domain in url_lower for domain in skip_domains):
            return False
            
        # Keywords that suggest a VC firm website
        vc_keywords = [
            'venture', 'capital', 'vc', 'invest', 'portfolio',
            'partners', 'fund', 'equity', 'ventures', 'seed',
            'accelerator', 'incubator', 'startup', 'innovation',
            'growth', 'series', 'angel', 'funding'
        ]
        
        return any(keyword in url_lower for keyword in vc_keywords)

    def save_urls(self) -> None:
        """Save gathered URLs to CSV file with backup"""
        # Create backup of existing file
        if os.path.exists(self.output_file):
            backup_file = f"{self.output_file}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            try:
                os.rename(self.output_file, backup_file)
                logger.info(f"Created backup: {backup_file}")
            except Exception as e:
                logger.error(f"Error creating backup: {e}")

        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['url'])  # Header
                for url in sorted(self.urls):
                    writer.writerow([url])
            logger.info(f"Saved {len(self.urls)} URLs to {self.output_file}")
            
            # Clean up checkpoint file after successful save
            if os.path.exists(self.checkpoint_file):
                os.remove(self.checkpoint_file)
                
        except Exception as e:
            logger.error(f"Error saving URLs: {e}")
            self.save_checkpoint()  # Ensure we don't lose data

if __name__ == "__main__":
    try:
        gatherer = VCUrlGatherer()
        gatherer.gather_urls()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
