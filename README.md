# Email Scraper with Scrapy

A Python-based web scraping project that extracts email addresses from web pages using the Scrapy framework and saves them into a CSV file.

## Features

- Starts crawling from a user-specified URL.
- Extracts valid email addresses using regex.
- Filters duplicate emails and excludes image-related addresses.
- Saves the results to a CSV file.

---

## Project Structure

email_scraper/ │ ├── email_scraper/ │ ├── spiders/ │ │ ├── email_spider.py # Main spider logic │ │ └── init.py │ ├── init.py │ ├── items.py │ ├── middlewares.py │ ├── pipelines.py │ └── settings.py ├── scrapy.cfg └── emails.csv # Output file (generated after running the spider)

yaml
Copy code

---

## Requirements

- **Python**: Version 3.8 or higher
- **Scrapy**: A Python framework for web scraping
- [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for managing environments

---

## Installation

Follow these steps to set up the project:

### 1. Install Anaconda or Miniconda

- Download and install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) based on your preference.

### 2. Create a New Environment

Run the following commands in your terminal or command prompt:

```bash
conda create -n email_scraper_env python=3.9 -y
conda activate email_scraper_env
3. Install Dependencies
With the environment activated, install Scrapy:

bash
Copy code
pip install scrapy
How to Run the Spider
Navigate to the project folder:

bash
Copy code
cd email_scraper
Start the spider with the target URL:

bash
Copy code
scrapy crawl email_spider -a url="https://example.com"
Output
Extracted emails will be saved to a CSV file in the project directory.
For example, if the URL is https://example.com, the output file will be named example_com_emails.csv.
How It Works
Code Overview
The main spider code (email_spider.py) does the following:

Crawls a website: Starting from the given URL, it extracts and follows links.
Extracts email addresses: Uses regex to identify valid email patterns.
Filters duplicates and invalid emails: Ensures only unique, valid email addresses are stored.
Saves results: Appends each extracted email to a CSV file.
Dependencies
Python 3.8 or higher
Scrapy framework
You can install these via the instructions in the Installation section.

Example Output
A sample output in the CSV file (example_com_emails.csv):

graphql
Copy code
email_ids
contact@example.com
info@website.org
admin@sampledomain.com
Notes
The project respects robots.txt rules by default (ROBOTSTXT_OBEY=True).
Use this tool responsibly and avoid scraping websites without permission.
Troubleshooting
1. scrapy: command not found
Ensure Scrapy is installed in your active environment.
Use the full Python command if needed:
bash
Copy code
python -m scrapy crawl email_spider -a url="https://example.com"
2. Missing Dependencies
Ensure all required dependencies are installed in the Conda environment.
Check the Python version:
bash
Copy code
python --version
License
This project is licensed under the MIT License.

yaml
Copy code

---

Feel free to save this file as `README.md` in your project directory! Let me know if you need furt
