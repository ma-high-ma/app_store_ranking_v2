import os

from scrapingbee import ScrapingBeeClient

from apps.app_rank.constants import SessionStatus, RETRY_MAX_ATTEMPTS
from apps.app_rank.exceptions import PageNotScrapedSuccessfully, AppPageScrapingMaxRetriesReached
from apps.app_rank.models import ScrapedHTML, ErrorLog
from apps.app_rank.services.SessionManager import SessionManagerService


class HTMLAppPageScraper:
    def __init__(self, session_id, app_handle):
        self.session_id = session_id
        self.app_handle = app_handle

    def get_client(self):
        try:
            print('inside client')
            return ScrapingBeeClient(api_key=os.environ['SCRAPING_BEE_API_KEY'])
        except Exception as e:
            print('inside client exception')
            error_msg = {
                'Exception': str(e),
                'details': f'Error occurred while getting ScrapingBee client'
            }
            SessionManagerService().process_failed_session(self.session_id, error_msg)

    def get_url(self):
        return 'https://apps.shopify.com'

    def get_response_object(self, url):
        attempts = 1
        while attempts <= RETRY_MAX_ATTEMPTS:
            print('attempt = ', attempts)
            try:
                response_obj = self.get_client().get(url, )
                if response_obj.status_code != 200:
                    raise PageNotScrapedSuccessfully(app_handle=self.app_handle)
                return response_obj
            except (PageNotScrapedSuccessfully, Exception) as e:
                ErrorLog.objects.create(
                    error_message=str(e),
                    session_id=self.session_id
                )
                attempts += 1
                continue
        if attempts == 4:
            raise AppPageScrapingMaxRetriesReached

    def scrape_page(self):
        SessionManagerService().update_session(
            session_id=self.session_id,
            status=SessionStatus.IN_PROGRESS
        )
        url = f'{self.get_url()}/{self.app_handle}/'
        print('app_handle = ', self.app_handle)

        try:
            response_object = self.get_response_object(url)
        except AppPageScrapingMaxRetriesReached as e:
            error_msg = {
                'Exception': str(e),
                'details': f'Error occurred while scraping app_handle = {self.app_handle}'
            }
            SessionManagerService().process_failed_session(self.session_id, error_msg)
            print('EXCEPTION: ', str(e))
            raise PageNotScrapedSuccessfully(app_handle=self.app_handle)
        else:
            ScrapedHTML.objects.create(app_handle=self.app_handle, content=response_object.content,
                                       session_id=self.session_id)
            SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED)
