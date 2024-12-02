
Email Scraper with Scrapy
=========================

A Python-based web scraping tool using Scrapy to extract email addresses from websites and save them in a CSV file.

--------------------------------------------------------------------------------
Angular D3 Repository
Check out another cool project: https://github.com/ansifi/angular-d3-tests

--------------------------------------------------------------------------------
Installation

1. Set Up Python Environment
Use Anaconda or Miniconda to manage your Python environment.

With Miniconda/Anaconda:
    conda create -n email_scraper_env python=3.8
    conda activate email_scraper_env

2. Install Dependencies
With the environment activated, install Scrapy:
    pip install scrapy

--------------------------------------------------------------------------------
How to Run the Spider

1. Navigate to the Project Folder:
    cd email_scraper

2. Start the Spider with the Target URL:
    scrapy crawl email_spider -a url="https://example.com"

--------------------------------------------------------------------------------
Output
Extracted emails will be saved to a CSV file in the project directory.

For example, if the URL is https://example.com, the output file will be named:
    example_com_emails.csv

--------------------------------------------------------------------------------
How It Works

Code Overview
The main spider code (email_spider.py) performs the following steps:
1. Crawls a website: Starting from the given URL, it extracts and follows internal links.
2. Extracts email addresses: Uses regex to identify valid email patterns.
3. Filters duplicates and invalid emails: Ensures only unique, valid email addresses are stored.
4. Saves results: Appends each extracted email to a CSV file.

--------------------------------------------------------------------------------
Dependencies
- Python 3.8 or higher
- Scrapy framework

Install dependencies using the instructions in the Installation section.

--------------------------------------------------------------------------------
Example Output
A sample output in the CSV file (example_com_emails.csv):

email_ids
contact@example.com
info@website.org
admin@sampledomain.com

--------------------------------------------------------------------------------
Notes
- The project respects robots.txt rules by default (ROBOTSTXT_OBEY=True).
- Use this tool responsibly and avoid scraping websites without permission.

--------------------------------------------------------------------------------
Troubleshooting

1. scrapy: command not found
Ensure Scrapy is installed in your active environment.
Use the full Python command if needed:
    python -m scrapy crawl email_spider -a url="https://example.com"

2. Missing Dependencies
Ensure all required dependencies are installed in the Conda environment.
Check the Python version:
    python --version

--------------------------------------------------------------------------------
License
This project is licensed under the MIT License.
