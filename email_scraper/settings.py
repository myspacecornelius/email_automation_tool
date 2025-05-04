# Scrapy settings for email_scraper project

BOT_NAME = 'email_scraper'

SPIDER_MODULES = ['email_scraper.spiders']
NEWSPIDER_MODULE = 'email_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) in the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performing at the same time to the same domain
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 2

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Configure item pipelines
ITEM_PIPELINES = {
}

# Enable and configure HTTP caching (disabled by default)
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncio.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

# Custom settings for email scraping
DEPTH_LIMIT = 3  # Limit crawl depth (ie, how many links deep to follow)
COOKIES_ENABLED = True
DOWNLOAD_TIMEOUT = 30 # Timeout for requests (ie, how long to wait for a response)
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429] # These HTTP codes will trigger a retry
