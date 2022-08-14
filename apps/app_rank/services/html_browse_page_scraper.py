import os

from scrapingbee import ScrapingBeeClient

from apps.app_rank.constants import SessionStatus
from apps.app_rank.exceptions import PageNotScrapedSuccessfully
from apps.app_rank.models import ScrapedHTML
from apps.app_rank.services.SessionManager import SessionManagerService


class HTMLBrowsePageScraper:
    def __init__(self, session_id):
        self.session_id = session_id
        self.scraped_html_objs = []

    def get_client(self):
        try:
            return ScrapingBeeClient(api_key=os.environ['SCRAPING_BEE_API_KEY'])
        except Exception as e:
            error_msg = {
                'Exception': str(e),
                'details': f'Error occurred while getting ScrapingBee client'
            }
            SessionManagerService().process_failed_session(self.session_id, error_msg)

    def get_url(self):
        return 'https://apps.shopify.com/browse'

    def remove_all_html_objects(self):
        ScrapedHTML.objects.all().delete()
        print('Deleted all current html data')

    def scrape_page(self, start_page_no, last_page_no):
        SessionManagerService().update_session(
            session_id=self.session_id,
            status=SessionStatus.IN_PROGRESS
        )
        self.remove_all_html_objects()
        client = self.get_client()
        url = self.get_url()
        for page in range(start_page_no, last_page_no + 1):
            try:
                print('page_no=', page)
                url_with_page_no = f'{url}?page={str(page)}'
                response_object = client.get(
                    url_with_page_no,
                )
                if response_object.status_code != 200:
                    raise PageNotScrapedSuccessfully(page_no=page)

                scraped_html_obj = ScrapedHTML(
                    page_no=page,
                    content=response_object.content,
                    session_id=self.session_id
                )
                self.scraped_html_objs.append(scraped_html_obj)

            except (PageNotScrapedSuccessfully, Exception) as e:
                error_msg = {
                    'Exception': str(e),
                    'details': f'Error occurred while scraping page no = {page}'
                }
                SessionManagerService().process_failed_session(self.session_id, error_msg)
                print('EXCEPTION: ', str(e))
                return
        ScrapedHTML.objects.bulk_create(self.scraped_html_objs)
        SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED)
        print('SCRAPING COMPLETE')
        return
