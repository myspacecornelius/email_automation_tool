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
