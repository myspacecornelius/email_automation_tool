import scrapy
import re
import os
import logging
from urllib.parse import urlparse

class EmailSpider(scrapy.Spider):
    name = "email_spider"

    # Set to store unique emails
    found_emails = set()

    custom_settings = {
        'ROBOTSTXT_OBEY': True,  # Ensures we obey robots.txt rules
        'LOG_LEVEL': 'INFO',  # Set logging level
    }

    def __init__(self, url=None, *args, **kwargs):
        super(EmailSpider, self).__init__(*args, **kwargs)
        if url:
            try:
                # Parse the domain from the URL and set it as the allowed domain
                parsed_url = urlparse(url)
                self.start_urls = [url]
                self.allowed_domains = [parsed_url.netloc]

                # Define the output folder and file
                self.external_folder = os.path.join('..', 'common_data')
                os.makedirs(self.external_folder, exist_ok=True)  # Create the folder if it doesn't exist
                self.output_file = os.path.join(self.external_folder, 'emails.csv')

                # Write headers if file doesn't exist
                if not os.path.exists(self.output_file):
                    self.write_headers()

                logging.info(f"Scraper initialized for URL: {url}")

            except Exception as e:
                self.start_urls = []
                self.allowed_domains = []
                logging.error(f"Error initializing scraper: {e}")
        else:
            self.start_urls = []
            self.allowed_domains = []
            logging.warning("No URL provided. Spider will not run.")

    def parse(self, response):
        try:
            # Extract email addresses from the current page using regex
            emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text))

            # Filter out invalid emails based on image-related keywords
            image_keywords = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '@2x']
            for email in emails:
                if not any(keyword in email.lower() for keyword in image_keywords):
                    if email not in self.found_emails:  # Only process unique emails
                        self.found_emails.add(email)
                        yield {'email_ids': email}  # Yield the email to be saved as CSV
                        self.save_email(email)  # Append email to file

            # Extract and follow internal links (only non-image links)
            links = response.css('a::attr(href)').getall()
            image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')

            for link in links:
                # Handle relative links and filter out images
                if not link.lower().endswith(image_extensions):
                    yield response.follow(link, callback=self.parse)

        except Exception as e:
            logging.error(f"Error parsing response from {response.url}: {e}")

    def write_headers(self):
        """Write headers to the file (if not exists)."""
        try:
            with open(self.output_file, 'w', newline='') as f:
                f.write('email_ids\n')  # Write the header for the email_ids column
            logging.info(f"Headers written to {self.output_file}")
        except Exception as e:
            logging.error(f"Error writing headers to {self.output_file}: {e}")

    def save_email(self, email):
        """Append the email to the external CSV file."""
        try:
            with open(self.output_file, 'a', newline='') as f:
                f.write(f"{email}\n")  # Save email under the 'email_ids' column
            logging.info(f"Saved email: {email}")
        except Exception as e:
            logging.error(f"Error saving email {email} to {self.output_file}: {e}")
