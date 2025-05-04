import time
import csv
import re
import logging
from typing import Set, List, Dict
from contextlib import contextmanager
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VCInvestorScraper:
    def __init__(self, urls: List[str], output_file: str = 'common_data/vc_investors_emails.csv'):
        self.urls = urls
        self.output_file = output_file
        self.ua = UserAgent()
        self.emails_found: Set[str] = set()
        self.results: List[Dict[str, str]] = []
        self.driver = None
        self.setup_driver()

    def setup_driver(self) -> None:
        """Initialize the Chrome WebDriver with proper error handling"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument(f'user-agent={self.ua.random}')
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--accept-language=en-US,en;q=0.9")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.ua.random})
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    @contextmanager
    def driver_context(self):
        """Context manager for WebDriver to ensure proper cleanup"""
        try:
            yield self.driver
        finally:
            if self.driver:
                self.driver.quit()

    def scrape(self) -> None:
        """Main scraping method with proper error handling and cleanup"""
        with self.driver_context():
            for url in self.urls:
                logger.info(f"Scraping {url}")
                try:
                    self.scrape_url(url)
                except Exception as e:
                    logger.error(f"Error processing {url}: {e}")
                self.apply_rate_limit()
            
            self.save_results()

    def scrape_url(self, url: str) -> None:
        """Scrape a single URL and its relevant pages"""
        self.driver.get(url)
        self.handle_cookie_consent()
        self.apply_rate_limit()
        
        self.scroll_page()
        relevant_urls = self.find_relevant_pages(url)
        
        for page_url in relevant_urls:
            try:
                self.driver.get(page_url)
                self.handle_cookie_consent()
                self.scroll_page()
                self.scrape_page(page_url)
            except Exception as e:
                logger.error(f"Error scraping {page_url}: {e}")
            self.apply_rate_limit()

    def handle_cookie_consent(self) -> None:
        """Handle cookie consent popups"""
        consent_selectors = [
            "//button[contains(text(), 'Accept')]",
            "//button[contains(text(), 'Accept All')]",
            "#onetrust-accept-btn-handler",
            ".cookie-consent-accept"
        ]
        
        for selector in consent_selectors:
            try:
                element = self.driver.find_element(
                    By.XPATH if selector.startswith("//") else By.CSS_SELECTOR,
                    selector
                )
                element.click()
                logger.info("Handled cookie consent popup")
                return
            except Exception:
                continue

    def scroll_page(self) -> None:
        """Scroll page to load dynamic content"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        except Exception as e:
            logger.error(f"Error scrolling page: {e}")

    def apply_rate_limit(self) -> None:
        """Apply rate limiting between requests"""
        time.sleep(2)  # Base delay
        if random.random() < 0.2:  # 20% chance of longer delay
            time.sleep(random.uniform(2, 4))

    def find_relevant_pages(self, base_url: str) -> Set[str]:
        """Find relevant pages to scrape using efficient URL checking"""
        relevant_urls = {base_url}
        base_domain = urlparse(base_url).netloc
        
        try:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            relevant_keywords = {'team', 'about', 'contact', 'people', 'partner', 'investor'}
            
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if not href:
                        continue
                    
                    parsed_url = urlparse(href)
                    if (parsed_url.netloc == base_domain and
                        any(keyword in href.lower() for keyword in relevant_keywords)):
                        relevant_urls.add(href)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Error finding relevant pages: {e}")
            
        return relevant_urls

    def scrape_page(self, url: str) -> None:
        """Scrape a single page for emails and information"""
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        self.extract_visible_emails(soup, url)
        self.extract_mailto_links(soup, url)
        self.extract_obfuscated_emails(soup, url)
        self.extract_from_scripts(soup, url)

    def extract_emails_from_text(self, text: str) -> Set[str]:
        """Extract and validate emails from text"""
        if not text:
            return set()
            
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = set(re.findall(email_pattern, text))
        return {email for email in emails if self.is_valid_email(email)}

    def extract_visible_emails(self, soup: BeautifulSoup, url: str) -> None:
        """Extract visible email addresses from text"""
        for text in soup.stripped_strings:
            for email in self.extract_emails_from_text(text):
                self.add_result(email, url)

    def extract_mailto_links(self, soup: BeautifulSoup, url: str) -> None:
        """Extract email addresses from mailto links"""
        for link in soup.select('a[href^="mailto:"]'):
            href = link.get('href', '')
            email = href.replace('mailto:', '').split('?')[0].strip()
            if self.is_valid_email(email):
                self.add_result(email, url)

    def extract_obfuscated_emails(self, soup: BeautifulSoup, url: str) -> None:
        """Handle common email obfuscation techniques"""
        for elem in soup.find_all(True):
            for value in elem.attrs.values():
                if isinstance(value, str) and '@' in value:
                    for email in self.extract_emails_from_text(value):
                        self.add_result(email, url)

    def extract_from_scripts(self, soup: BeautifulSoup, url: str) -> None:
        """Extract emails from script tags"""
        for script in soup.find_all('script'):
            if script.string:
                for email in self.extract_emails_from_text(script.string):
                    self.add_result(email, url)

    def is_valid_email(self, email: str) -> bool:
        """Validate email address with simplified checks"""
        if not email or len(email) > 254:
            return False
            
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False
            
        # Check for common invalid patterns
        invalid_domains = {'example.com', 'test.com', 'domain.com'}
        domain = email.split('@')[-1].lower()
        
        return domain not in invalid_domains

    def add_result(self, email: str, url: str) -> None:
        """Add a new result to the collection"""
        if email not in self.emails_found:
            self.emails_found.add(email)
            firm_name = self.extract_firm_name(url)
            self.results.append({
                'email': email,
                'firm_name': firm_name,
                'url': url,
                'additional_info': self.extract_additional_info(url)
            })
            logger.info(f"Found email: {email} at {url}")

    def extract_firm_name(self, url: str) -> str:
        """Extract firm name from the page"""
        try:
            # Try schema.org data
            elements = self.driver.find_elements(By.CSS_SELECTOR, '[typeof="Organization"][property="name"]')
            if elements:
                return elements[0].text.strip()
            
            # Try title
            title = self.driver.title
            if title:
                for suffix in [' - Home', ' - Contact', ' - About', ' | Contact', ' | About']:
                    title = title.replace(suffix, '')
                return title.strip()
        except Exception:
            pass
        
        # Fallback to URL
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0].title()

    def extract_additional_info(self, url: str) -> str:
        """Extract additional relevant information"""
        info = []
        try:
            # Meta description
            elements = self.driver.find_elements(By.CSS_SELECTOR, "meta[name='description']")
            if elements:
                info.append(elements[0].get_attribute('content'))
            
            # Investment focus
            keywords = ['investment focus', 'investment strategy', 'what we invest in']
            for keyword in keywords:
                elements = self.driver.find_elements(
                    By.XPATH,
                    f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword}')]"
                )
                for elem in elements:
                    info.append(elem.text.strip())
        except Exception as e:
            logger.error(f"Error extracting additional info: {e}")
        
        return ' | '.join(filter(None, info))

    def save_results(self) -> None:
        """Save results to CSV file with proper error handling"""
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['email', 'firm_name', 'url', 'additional_info'])
                writer.writeheader()
                writer.writerows(self.results)
            logger.info(f"Saved {len(self.results)} emails to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")

if __name__ == '__main__':
    import random
    test_urls = [
        'https://www.sequoiacap.com',
        'https://www.accel.com',
        'https://www.benchmark.com'
    ]
    
    try:
        scraper = VCInvestorScraper(test_urls)
        scraper.scrape()
    except Exception as e:
        logger.error(f"Scraper failed: {e}")
