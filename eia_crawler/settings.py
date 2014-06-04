# Scrapy settings for eia_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eia_crawler'

SPIDER_MODULES = ['eia_crawler.spiders']
NEWSPIDER_MODULE = 'eia_crawler.spiders'

DOWNLOAD_DELAY = 5

CONCURRENT_REQUESTS = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eia_crawler (+http://www.yourdomain.com)'
