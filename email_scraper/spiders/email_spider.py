import scrapy
import re
import os
from urllib.parse import urlparse

class EmailSpider(scrapy.Spider):
    name = "email_spider"

    # Set to store unique emails
    found_emails = set()

    custom_settings = {
        'ROBOTSTXT_OBEY': True,  # Ensures we obey robots.txt rules
    }
    
    def __init__(self, url=None, *args, **kwargs):
        super(EmailSpider, self).__init__(*args, **kwargs)
        if url:
            # Parse the domain from the URL and set it as the allowed domain
            parsed_url = urlparse(url)
            self.start_urls = [url]
            self.allowed_domains = [parsed_url.netloc]
            # Generate the filename from the domain
            self.output_file = f"{parsed_url.netloc.replace('.', '_')}_emails.csv"
            
            # Write headers if file doesn't exist
            if not os.path.exists(self.output_file):
                self.write_headers()

        else:
            self.start_urls = []
            self.allowed_domains = []

    def parse(self, response):
        # Extract email addresses from the current page
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text))
        
        # Filter out emails that resemble image file names
        image_keywords = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '@2x']
        
        for email in emails:
            if not any(keyword in email.lower() for keyword in image_keywords):
                if email not in self.found_emails:  # Only process unique emails
                    self.found_emails.add(email)
                    yield {'email_ids': email}
                    # Save the email to the file
                    self.save_email(email)

        # Extract and follow internal links
        links = response.css('a::attr(href)').getall()
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')

        for link in links:
            # Skip links that point to images
            if not link.lower().endswith(image_extensions):
                # Use response.follow to handle both relative and absolute links
                yield response.follow(link, callback=self.parse)

    def write_headers(self):
        # Write headers (email_ids, name, company) to the file
        with open(self.output_file, 'w') as f:
            f.write('email_ids\n')

    def save_email(self, email):
        # Append the email to the file with blank name and company fields
        with open(self.output_file, 'a') as f:
            f.write(f"{email}\n")
