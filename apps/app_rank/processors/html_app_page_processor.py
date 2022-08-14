from bs4 import BeautifulSoup

from apps.app_rank.constants import SessionStatus
from apps.app_rank.models import ScrapedHTML, ShopifyApp, AppData
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.app_rank.services.basic_utils import BasicUtils


class HTMLAppPageProcessor:
    def __init__(self, session_id, app_handle=None):
        self.session_id = session_id
        self.app_handle = app_handle
        self.app_data_objs = []
        if self.app_handle is not None:
            self.app = ShopifyApp.objects.filter(app_handle=self.app_handle).first()
            assert self.app is not None
            html_app_page_obj = ScrapedHTML.objects.get(app_handle=self.app_handle)
            self.soup = BeautifulSoup(html_app_page_obj.content, features="html.parser")
        else:
            self.soup = None

    def get_categories_list(self):
        html_categories_ul = self.soup.find('ul', {'class': 'vc-app-listing-hero__taxonomy-links'})
        if html_categories_ul is None:
            return []

        list_items = html_categories_ul.find_all('li')

        # Process list_items
        categories = []
        for li in list_items:
            categories.append(BasicUtils.get_text_from_html_element(li))
        return categories

    def get_signifiers_list(self):
        signifiers_block_html = self.soup.find('div', {'class': 'vc-verified-attributes-section__block'})
        if signifiers_block_html is None:
            return []

        signifiers_html = signifiers_block_html.find_all('p', {'class': 'vc-verified-attributes-section__item-text'})

        signifiers = []

        for each_signifier_html in signifiers_html:
            signifiers.append(BasicUtils.get_text_from_html_element(each_signifier_html))
        return signifiers

    def get_review_dict(self):
        review_rating_html = self.soup.find('div', {'class': 'reviews-summary'})

        r = review_rating_html.find('span', {'class': 'ui-star-rating__rating'}).text
        review_rating = float(r.split()[0])

        review_count_html = self.soup.find('span', {'class': 'ui-review-count-summary'}).text
        review_count = int(review_count_html.split()[0])

        return {
            'review_rating': review_rating,
            'review_count': review_count
        }

    def get_pricing_dict(self):
        price_listing_sub_heading = self.soup.find('span', {'class': 'app-listing-title__sub-heading'})
        res = {'price_listing_sub_heading': BasicUtils.get_text_from_html_element(price_listing_sub_heading)}

        pricing_cards = self.soup.find_all('div', {'class': 'pricing-plan-card'})
        if pricing_cards is None:
            return res
        for index, each_card in enumerate(pricing_cards):
            p_price = each_card.find('h3', {'class': 'pricing-plan-card__title-header'})
            p_name = each_card.find('p', {'class': 'pricing-plan-card__title-kicker'})
            p_sub_heading = each_card.find('p', {'class': 'pricing-plan-card__title-sub-heading'})

            x = {
                'title': BasicUtils.get_text_from_html_element(p_name),
                'price': BasicUtils.get_text_from_html_element(p_price),
                'sub-heading': BasicUtils.get_text_from_html_element(p_sub_heading)
            }
            res[f'card-{index + 1}'] = x
        return res

    def get_app_tagline(self):
        tagline = self.soup.find('p', {'class': 'vc-app-listing-hero__tagline'})
        return BasicUtils.get_text_from_html_element(tagline)

    def get_extras(self, data=None):
        if data is None:
            data = {}
        return {
            'app_tagline': self.get_app_tagline(),
            **data
        }

    def process_single_app_page(self, bulk=False):
        print('processing app = ', self.app_handle)
        categories = self.get_categories_list()
        signifiers = self.get_signifiers_list()
        review = self.get_review_dict()
        pricing = self.get_pricing_dict()

        res = {
            'shopify_app_id': self.app_handle,
            'reviews_count': review['review_count'],
            'reviews_rating': review['review_rating'],
            'signifiers': signifiers,
            'categories': categories,
            'pricing': pricing,
            'extras': self.get_extras()
        }
        if bulk:
            app_data_obj = AppData(
                hash=BasicUtils.get_dict_hash(res),
                **res
            )
            self.app_data_objs.append(app_data_obj)
        else:
            AppData.objects.create(
                hash=BasicUtils.get_dict_hash(res),
                **res
            )

    def process_all_app_html_pages(self):
        SessionManagerService().update_session(self.session_id, SessionStatus.IN_PROGRESS)

        if self.app_handle is not None:
            try:
                self.process_single_app_page()
            except Exception as e:
                error_msg = {
                    'Exception': str(e),
                    'details': f'Error occurred while processing single app = {self.app_handle}'
                }
                SessionManagerService().process_failed_session(self.session_id, error_msg)
                return
        else:
            all_app_pages = ScrapedHTML.objects.all()
            for each_app_page in all_app_pages:
                try:
                    self.app_handle = each_app_page.app_handle
                    self.app = ShopifyApp.objects.get(app_handle=self.app_handle)
                    assert self.app_handle is not None
                    self.soup = BeautifulSoup(each_app_page.content, features="html.parser")
                    self.process_single_app_page(bulk=True)
                    AppData.objects.bulk_create(self.app_data_objs)
                except Exception as e:
                    error_msg = {
                        'Exception': str(e),
                        'details': f'Error occurred while processing app = {self.app_handle}'
                    }
                    SessionManagerService().process_failed_session(self.session_id, error_msg)
        SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED)
