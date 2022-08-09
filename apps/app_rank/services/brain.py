from apps.app_rank.constants import SessionType
from apps.app_rank.models import Keyword
from apps.app_rank.processors.html_browse_page_processor import HTMLBrowsePageProcessor
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.app_rank.services.html_browse_page_scraper import HTMLBrowsePageScraper


class Brain:
    def logic(self):
        # Global App Rank
        keyword = Keyword.objects.get_or_create(keyword='global')

        # Scrape HTML of browse apps page
        session_id = SessionManagerService.create_session(SessionType.HTML_SCRAPER)
        HTMLBrowsePageScraper(session_id).scrape_page(
            start_page_no=1,
            last_page_no=5
        )

        # Process HTML app store pages
        session_id = SessionManagerService.create_session(SessionType.HTML_PROCESSOR)
        HTMLBrowsePageProcessor(session_id=session_id, keyword=keyword).process()
        