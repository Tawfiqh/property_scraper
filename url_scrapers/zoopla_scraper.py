from models import Property, UrlToScrape
from url_scrapers.property_scraper import PropertyScraper

class ZooplaScraper(PropertyScraper):
    def __init__(self, db_session) -> None:
        self.property_scraper='Zoopla'
        super().__init__(db_session)


    def scrape_url(self, url):
        print(f"TODO {self.property_scraper}: scrape url {url}")
