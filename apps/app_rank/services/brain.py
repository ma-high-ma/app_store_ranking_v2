import time

import schedule

from apps.app_rank.constants import SessionType, SessionStatus
from apps.app_rank.models import Keyword, Session
from apps.app_rank.processors.app_data_delta_processor import AppDataDeltaProcessor
from apps.app_rank.processors.app_rank_processor import AppRankProcessor
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.scrapers.html_category_wise_scraper import HTMLCategoryWiseScraper


class Brain:
    def cron_logic(self, keyword_title='global'):
        session_ids = []
        # Global App Rank

        keyword, created = Keyword.objects.get_or_create(keyword=keyword_title)
        # 'store-management'

        session_id = SessionManagerService.create_session(SessionType.HTML_SCRAPER)
        session_ids.append(session_id)
        HTMLCategoryWiseScraper(session_id, keyword=keyword.keyword).scrape_page(
            start_page_no=1,
            last_page_no=5
        )

        session_id = SessionManagerService.create_session(SessionType.APP_RANK_PROCESSOR)
        session_ids.append(session_id)
        AppRankProcessor(session_id=session_id, keyword_id=keyword.id).process()

        # Process app data delta for apps whose ranks have changed
        session_id = SessionManagerService.create_session(SessionType.APP_DATA_DELTA_PROCESSOR)
        session_ids.append(session_id)
        AppDataDeltaProcessor(session_id=session_id).process()

        session_objs = Session.objects.filter(id__in=session_ids)
        for each_obj in session_objs:
            if each_obj.status not in (SessionStatus.COMPLETED, SessionStatus.FAILED):
                each_obj.status = SessionStatus.INCOMPLETE
                each_obj.save()


def process():
    keywords = Keyword.objects.all().values_list('keyword')
    for each_keyword in keywords:
        Brain().cron_logic(keyword_title=each_keyword)


job = schedule.every().day.at("8:16").do(process)

while True:
    schedule.run_pending()
    time.sleep(1)
