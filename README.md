# Enhanced VC Email Automation Tool

A Python-based automation tool specialized in gathering VC investor contact information, with support for both simple email scraping and advanced VC-specific data collection.

## Directory Structure

```
email_automation_tool/
├── common_data/              # Shared data directory
│   ├── emails.csv           # General email scraping results
│   └── vc_investors_emails.csv  # VC-specific results with additional info
│
├── email_campaign/          # Email campaign functionality
│   ├── send_email.py       # Email sending logic
│   └── templates/          # Email templates
│       └── email_form.html
│
├── email_scraper/          # Core scraping functionality
│   ├── spiders/           # Scrapy spiders
│   │   └── email_spider.py  # Basic email spider
│   ├── vc_investor_scraper.py  # Advanced VC-specific scraper
│   ├── vc_url_gatherer.py  # VC firm URL discovery
│   └── settings.py        # Scrapy settings
│
├── email_tool.py          # Main CLI tool
├── requirements.txt       # Project dependencies
└── scrapy.cfg            # Scrapy configuration
```

## Installation

1. Set up Python environment:
```bash
conda create -n vc_scraper_env python=3.8
conda activate vc_scraper_env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Email Scraping
For simple email collection from a website:
```bash
python email_tool.py --url "https://example.com"
```

### VC-Specific Scraping
For comprehensive VC investor data collection:

```bash
# Scrape a specific VC firm website
python email_tool.py --vc --url "https://vc-firm-website.com"

# Auto-discover and scrape multiple VC firms
python email_tool.py --vc

# Scrape without running email campaign
python email_tool.py --vc --url "https://vc-firm-website.com" --no-campaign
```

## Features

### URL Discovery (New!)
- Extensive VC directory coverage
- Global and regional VC associations
- Industry-specific directories
- Angel/seed networks
- Accelerator networks
- Checkpoint system for reliable gathering
- Rate limiting and retry logic
- Progress tracking and logging

### Email Scraping
- Basic email pattern matching
- JavaScript-rendered content support
- Cookie consent handling
- Rate limiting and retry logic
- Respects robots.txt

### VC-Specific Features
- Automatic VC firm discovery
- Team/contact page detection
- Advanced email extraction methods
- Additional data collection (firm name, focus areas)
- Contact form detection

### Email Campaign
- HTML email templates
- Customizable messaging
- Campaign tracking

## Output Format

### Basic Mode (emails.csv)
```csv
email_ids
example@domain.com
```

### VC Mode (vc_investors_emails.csv)
```csv
email,firm_name,url,additional_info
investor@vc.com,Acme VC,https://acmevc.com,Focuses on Series A
```

## Configuration

### URL Gatherer Settings
The VC URL gatherer (`vc_url_gatherer.py`) supports:
- Checkpoint files for resuming interrupted runs
- Configurable rate limiting
- Extensive logging
- Backup creation
- Progress tracking

### Scraping Settings
Edit `email_scraper/settings.py` to modify:
- Crawl depth
- Request delays
- Concurrent requests
- User agent
- Cache settings

### Email Settings
Configure email campaign settings in `email_campaign/send_email.py`

## Best Practices

1. **Rate Limiting**: Default settings include polite delays between requests
2. **Verification**: Always verify emails before sending campaigns
3. **Compliance**: Respect website terms of service and robots.txt
4. **Data Privacy**: Handle collected information responsibly
5. **Resumable Operations**: Use checkpoint system for large scraping tasks

## Troubleshooting

1. **URL Gathering Issues**
   - Check logs in vc_url_gatherer.log
   - Verify network connectivity
   - Check for rate limiting
   - Use checkpoint files to resume

2. **No Emails Found**
   - Check URL accessibility
   - Verify JavaScript rendering
   - Check rate limiting

3. **Email Campaign Issues**
   - Verify SMTP settings
   - Check email template formatting
   - Ensure valid email addresses

## License

MIT License - Feel free to use and modify for your projects.
