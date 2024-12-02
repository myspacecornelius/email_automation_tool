# Email Scraper with Scrapy

A Python-based web scraping project that extracts email addresses from web pages using the Scrapy framework and saves them into a CSV file.

## Features

- Starts crawling from a user-specified URL.
- Extracts valid email addresses using regex.
- Filters duplicate emails and excludes image-related addresses.
- Saves the results to a CSV file.

## Project Structure

email_scraper/ │ ├── email_scraper/ │ ├── spiders/ │ │ ├── email_spider.py

# Main spider logic │ │ └── init.py │ ├── init.py │ ├── items.py │ ├── middlewares.py │ ├── pipelines.py │ └── settings.py ├── scrapy.cfg └── emails.csv # Output file (generated after running the spider)


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
bash


