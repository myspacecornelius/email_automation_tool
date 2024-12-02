# Email Automation tool with Scrapy

A Python-based web email automation tool using Scrapy to extract email addresses from websites and send email via a CSV file.

## Installation

### 1. Set Up Python Environment
Use **Anaconda** or **Miniconda** to manage your Python environment.

#### With Miniconda/Anaconda:
1. Create and Activate the Conda Environment

Run the following commands:

```bash
conda create -n email_scraper_env python=3.8
conda activate email_scraper_env
```

2. Install Dependencies
With the environment activated, install Scrapy:

```bash
pip install scrapy
```

How to Run the Spider
1. Navigate to the Project Folder:
```bash
cd email_scraper
```

2. Start the Spider with the Target URL:
```bash
scrapy crawl email_spider -a url="https://example.com"
```

Output
Extracted emails will be saved to a CSV file in the project directory.

For example, if the URL is https://example.com, the output file will be named: example_com_emails.csv

How It Works

Code Overview
The main spider code (email_spider.py) performs the following steps:

Crawls a website: Starting from the given URL, it extracts and follows internal links.
Extracts email addresses: Uses regex to identify valid email patterns.
Filters duplicates and invalid emails: Ensures only unique, valid email addresses are stored.
Saves results: Appends each extracted email to a CSV file.

Dependencies

Python 3.8 or higher
Scrapy framework
Install dependencies using the instructions in the Installation section.

Example Output
A sample output in the CSV file (example_com_emails.csv):

```bash
email_ids
contact@example.com
info@website.org
admin@sampledomain.com
```
Automation of Email Campaign
Email Tool
The email automation process includes two key components:

Scraping Email Addresses: Scrapy will crawl the specified website(s), extract email addresses, and save them in a CSV file (emails.csv). This file will be used in the next step for sending emails.

Running Email Campaign: Once email addresses are scraped and saved in the CSV file, an email campaign is triggered automatically using the collected email data. The campaign is managed using the send_email.py script.

Workflow Overview
The email automation workflow follows these steps:

Run the Scraper: The scraper is executed by calling the scrapy crawl email_spider command. It extracts emails from the provided website URL and stores them in a CSV file.

Validate and Proceed with Campaign: The tool checks if the emails.csv file exists and contains valid email addresses. If the file is non-empty, the email campaign proceeds. If not, the process is halted, and no emails are sent.

Send Emails: If valid emails are found, the send_email.py script is triggered to send an email to each address in the CSV file.

Email Tool Script Overview
The main script (email_tool.py) automates the entire process by executing the following functions:

run_scraper: Executes the Scrapy spider to scrape emails from a given website.
run_email_campaign: Executes the email campaign using the send_email.py script.
main: Orchestrates the entire process by first running the scraper, then checking for the existence of the CSV file, and finally triggering the email campaign if valid email addresses are found.
Here is a simplified version of the email_tool.py:

```bash
import os
import subprocess

def run_scraper():
    print("Running email scraper...")
    subprocess.run(['scrapy', 'crawl', 'email_spider'], cwd=os.path.join('email_scraper'))
    print("Email scraper finished.")

def run_email_campaign():
    print("Running email campaign...")
    subprocess.run(['python', 'send_email.py'], cwd=os.path.join('email_campaign'))

def main():
    # Path to the shared emails.csv file
    data_file = os.path.join('common_data', 'emails.csv')
    
    # Step 1: Run the scraper
    run_scraper()
    
    # Step 2: Check if emails.csv is non-empty
    if os.path.exists(data_file) and os.stat(data_file).st_size > 0:
        print("Emails found. Proceeding with email campaign...")
        run_email_campaign()
    else:
        print("No emails found. Skipping email campaign.")

if __name__ == '__main__':
    main()
```

Notes
The project respects robots.txt rules by default (ROBOTSTXT_OBEY=True).
Use this tool responsibly and avoid scraping websites without permission.

Troubleshooting
1. scrapy: command not found
Ensure Scrapy is installed in your active environment. Use the full Python command if needed:

```bash
python -m scrapy crawl email_spider -a url="https://example.com"
```

2. Missing Dependencies
Ensure all required dependencies are installed in the Conda environment. Check the Python version:

```bash
python --version
```
This will make it easy for anyone to use and understand your project directly from GitHub.
