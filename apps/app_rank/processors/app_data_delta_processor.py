from apps.app_rank.constants import SessionType, SessionStatus
from apps.app_rank.exceptions import NoPreviousAppDataPresent, NoCompletedRankDeltaProcessorFound, \
    TaskInterruptedDueToAnException
from apps.app_rank.models import Session, RankDelta, ScrapedHTML, AppData
from apps.app_rank.processors.html_app_page_processor import HTMLAppPageProcessor
from apps.app_rank.services.SessionManager import SessionManagerService
from apps.scrapers.html_app_page_scraper import HTMLAppPageScraper


class AppDataDeltaProcessor:
    def __init__(self, session_id):
        self.session_id = session_id

    def __process(self):
        SessionManagerService().update_session(self.session_id)

        latest_rank_delta_processor_session = Session.objects.filter(
            type=SessionType.APP_RANK_PROCESSOR,
            status=SessionStatus.COMPLETED
        ).order_by('-created_at').first()

        print(latest_rank_delta_processor_session)

        if latest_rank_delta_processor_session is None:
            raise NoCompletedRankDeltaProcessorFound

        rank_delta_objs = RankDelta.objects.filter(session_id=latest_rank_delta_processor_session.id)
        app_handles = rank_delta_objs.values_list(
            'shopify_app_id', flat=True)

        print('app_handles = ', app_handles)

        # Delete all scraped HTML entries
        ScrapedHTML.objects.all().delete()

        for app_handle in app_handles:
            HTMLAppPageScraper(self.session_id, app_handle).scrape_page()
        print('scraping complete')

        # Store app data of all apps whose rank have changed
        HTMLAppPageProcessor(session_id=self.session_id).process_all_app_html_pages()

        # Check if app_data has changed and update AppRank table accordingly
        for app_handle in app_handles:
            try:
                app_data_qs = AppData.objects.filter(shopify_app_id=app_handle).order_by('-created_at')
                print(app_data_qs)
                if len(app_data_qs) < 2:
                    raise NoPreviousAppDataPresent(app_handle)

                app_rank_delta_obj = rank_delta_objs.get(shopify_app_id=app_handle)
                if app_data_qs[0].hash != app_data_qs[1].hash:
                    app_rank_delta_obj.has_app_data_changed = True
                    app_rank_delta_obj.save()

            except NoPreviousAppDataPresent as e:
                error_msg = {
                    'Exception': str(e),
                    'app_handle': app_handle,
                    'details': f'Error occurred during app data delta processing'
                }
                SessionManagerService().process_failed_session(self.session_id, error_msg)
                continue

        SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED)

    def process(self):
        try:
            self.__process()
        except (NoCompletedRankDeltaProcessorFound, Exception) as e:
            error_msg = {
                'Exception': str(e),
                'details': f'Error occurred during app data delta processing'
            }
            SessionManagerService().process_failed_session(self.session_id, error_msg)
            raise TaskInterruptedDueToAnException
