import os
import sys
import subprocess
import argparse
from email_scraper.vc_url_gatherer import VCUrlGatherer
from email_scraper.vc_investor_scraper import VCInvestorScraper

def run_scraper(url=None, vc_mode=False):
    print("Running email scraper...")
    if vc_mode:
        print("Using VC-specific scraper...")
        if url:
            # Run VC-specific scraper with single URL
            print("\nScraping specific URL...")
            urls = [url]
            scraper = VCInvestorScraper(urls)
            scraper.scrape()
        else:
            # Gather VC firm URLs
            print("Gathering VC firm URLs...")
            gatherer = VCUrlGatherer()
            gatherer.gather_urls()
            
            # Read gathered URLs
            with open('email_scraper/vc_firms_urls.csv', 'r') as f:
                next(f)  # Skip header
                urls = [line.strip() for line in f]
            
            # Run VC-specific scraper
            scraper = VCInvestorScraper(urls)
            scraper.scrape()
    else:
        # Run regular email spider
        cmd = ['scrapy', 'crawl', 'email_spider']
        if url:
            cmd.extend(['-a', f'url={url}'])
        subprocess.run(cmd, cwd=os.path.join('email_scraper'))
    print("Email scraper finished.")

def run_email_campaign():
    print("Running email campaign...")
    subprocess.run([sys.executable, 'send_email.py'], cwd=os.path.join('email_campaign'))

def main():
    parser = argparse.ArgumentParser(description='Email Automation Tool')
    parser.add_argument('--url', help='URL to scrape')
    parser.add_argument('--vc', action='store_true', help='Use VC-specific scraper')
    parser.add_argument('--no-campaign', action='store_true', help='Skip email campaign')
    args = parser.parse_args()
    
    # Path to the output file
    data_file = os.path.join('common_data', 'vc_investors_emails.csv' if args.vc else 'emails.csv')
    
    # Step 1: Run the scraper
    run_scraper(args.url, args.vc)
    
    # Step 2: Check if emails were found and run campaign if requested
    if os.path.exists(data_file) and os.stat(data_file).st_size > 0:
        print(f"Emails found in {data_file}")
        if not args.no_campaign:
            print("Proceeding with email campaign...")
            run_email_campaign()
        else:
            print("Skipping email campaign as requested.")
    else:
        print("No emails found. Skipping email campaign.")

if __name__ == '__main__':
    main()
