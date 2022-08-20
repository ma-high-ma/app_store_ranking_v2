from apps.app_rank.constants import SessionType, SessionStatus
from apps.app_rank.exceptions import PageNotScrapedSuccessfully
from apps.app_rank.models import Keyword, ScrapedHTML, ShopifyApp, Session
from apps.app_rank.processors.app_data_delta_processor import AppDataDeltaProcessor
from apps.app_rank.processors.app_rank_processor import AppRankProcessor
from apps.app_rank.processors.html_app_page_processor import HTMLAppPageProcessor
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.app_rank.services.html_app_page_scraper import HTMLAppPageScraper
from apps.app_rank.services.html_browse_page_scraper import HTMLBrowsePageScraper


class Brain:
    def cron_logic(self):
        session_ids = []
        # Global App Rank

        keyword, created = Keyword.objects.get_or_create(keyword='global')

        # Scrape HTML of browse apps page
        session_id = SessionManagerService.create_session(SessionType.HTML_SCRAPER)
        session_ids.append(session_id)
        HTMLBrowsePageScraper(session_id).scrape_page(
            start_page_no=1,
            last_page_no=5
        )

        session_id = SessionManagerService.create_session(SessionType.APP_RANK_PROCESSOR)
        session_ids.append(session_id)
        AppRankProcessor(session_id=session_id, keyword_id=keyword.id).process()

        # # Process HTML app store pages
        # session_id = SessionManagerService.create_session(SessionType.HTML_PROCESSOR)
        # session_ids.append(session_id)
        # HTMLBrowsePageProcessor(session_id=session_id, keyword_id=keyword.id).process()
        #
        # # Process Rank delta against last scraping session based on the keyword
        # session_id = SessionManagerService.create_session(SessionType.RANK_DELTA_PROCESSOR)
        # session_ids.append(session_id)
        # RankDeltaProcessor(session_id=session_id, keyword_id=keyword.id).process()

        # Process app data delta for apps whose ranks have changed
        session_id = SessionManagerService.create_session(SessionType.APP_DATA_DELTA_PROCESSOR)
        session_ids.append(session_id)
        AppDataDeltaProcessor(session_id=session_id).process()

        session_objs = Session.objects.filter(id__in=session_ids)
        for each_obj in session_objs:
            if each_obj.status not in (SessionStatus.COMPLETED, SessionStatus.FAILED):
                each_obj.status = SessionStatus.INCOMPLETE
                each_obj.save()


def adhoc_app_data_processor_logic(self):
    # Scrape all App HTML Pages
    session_id = SessionManagerService.create_session(SessionType.HTML_SCRAPER)
    ScrapedHTML.objects.all().delete()
    app_handles = ShopifyApp.objects.all().values_list('app_handle', flat=True)

    for app_handle in app_handles:
        try:
            HTMLAppPageScraper(session_id, app_handle).scrape_page()
        except PageNotScrapedSuccessfully as e:
            break

    # Process all App HTML Pages
    session_id = SessionManagerService.create_session(SessionType.HTML_PROCESSOR)
    HTMLAppPageProcessor(session_id=session_id).process_all_app_html_pages()
