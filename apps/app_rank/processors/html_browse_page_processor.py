from urllib import parse

from bs4 import BeautifulSoup

from apps.app_rank.constants import ScrapedHTMLStatus, SessionType
from apps.app_rank.models import ScrapedHTML, ShopifyApp, AppRank
from apps.app_rank.processors.html_app_page_processor import HTMLAppPageProcessor
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.app_rank.services.html_app_page_scraper import HTMLAppPageScraper


class HTMLBrowsePageProcessor:
    def __init__(self, session_id, keyword_id):
        self.session_id = session_id
        self.keyword_id = keyword_id
        self.app_ranks = []

    def __get_shopify_app_obj(self, app_handle, app_card):
        shopify_app = ShopifyApp.objects.filter(app_handle=app_handle).first()
        if shopify_app is None:
            app_name = app_card.find('p', {'class': 'ui-app-card__name'}).text
            developed_by = app_card.find('div', {'class': 'ui-app-card__developer-name'}).text
            shopify_app = ShopifyApp.objects.create(
                app_handle=app_handle,
                name=app_name,
                developed_by=developed_by
            )
            self.create_app_data(app_handle)
        return shopify_app

    def create_app_data(self, app_handle):
        HTMLAppPageScraper(self.session_id, app_handle).scrape_page()
        HTMLAppPageProcessor(self.session_id, app_handle).process_single_app_page()
        ScrapedHTML.objects.get(app_handle=app_handle).delete()

    def process_each_page(self, page_no, html_page_obj):
        print('page_no = ', page_no)

        soup = BeautifulSoup(html_page_obj.content, features="html.parser")
        all_app_cards_of_the_page = soup.find_all('div', {'class': 'ui-app-card'})

        for app_card in all_app_cards_of_the_page:
            rank = (24 * (page_no - 1)) if page_no != 1 else 0

            first_link = app_card['data-target-href']
            parsed_url = parse.urlparse(first_link)

            app_handle = parsed_url.path[1:]

            query_params = parse.parse_qs(parsed_url.query)
            rank += int(query_params['surface_intra_position'][0])

            app_rank_obj = AppRank(
                shopify_app=self.__get_shopify_app_obj(app_handle, app_card),
                rank=rank,
                keyword_id=self.keyword_id,
                session_id=self.session_id
            )
            self.app_ranks.append(app_rank_obj)

    def process(self):
        SessionManagerService().update_session(session_id=self.session_id,
                                               details=f'{SessionType.HTML_PROCESSOR} has begun')
        all_pages = ScrapedHTML.objects.all()
        for each_page in all_pages:
            try:
                each_page.status = ScrapedHTMLStatus.IN_PROGRESS
                each_page.save()
                self.process_each_page(
                    page_no=each_page.page_no,
                    html_page_obj=each_page
                )
                each_page.status = ScrapedHTMLStatus.PROCESSED
                each_page.save()
            except Exception as e:
                error_msg = {
                    'Exception': str(e),
                    'Location': SessionType.HTML_PROCESSOR,
                    'details': f'Error occurred while processing page no = {each_page.page_no}'
                }
                SessionManagerService().process_failed_session(self.session_id, error_msg)
                return
        AppRank.objects.bulk_create(self.app_ranks)
        SessionManagerService().update_session(session_id=self.session_id,
                                               details=f'{SessionType.HTML_PROCESSOR} has completed')
