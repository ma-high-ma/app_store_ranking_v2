from apps.scrapers.html_browse_page_scraper import HTMLBrowsePageScraper


class HTMLCategoryWiseScraper(HTMLBrowsePageScraper):
    def __init__(self, session_id, keyword):
        super().__init__(session_id=session_id)
        self.keyword = keyword

    def get_url(self):
        if self.keyword == 'global':
            return f'https://apps.shopify.com/browse/'
        return f'https://apps.shopify.com/browse/{self.keyword}/'
