from apps.app_rank.constants import SessionStatus, SessionType
from apps.app_rank.processors.html_browse_page_processor import HTMLBrowsePageProcessor
from apps.app_rank.processors.rank_delta_processor import RankDeltaProcessor
from apps.app_rank.services.SessionManager import SessionManagerService


class AppRankProcessor:
    def __init__(self, session_id, keyword_id):
        print('init = ', session_id)
        self.session_id = session_id
        self.keyword_id = keyword_id

    def process(self):
        print('session in app rank processor = ', self.session_id)
        SessionManagerService().update_session(self.session_id, SessionStatus.IN_PROGRESS,
                                               details=f'{SessionType.APP_RANK_PROCESSOR} has begun')

        HTMLBrowsePageProcessor(session_id=self.session_id, keyword_id=self.keyword_id).process()
        RankDeltaProcessor(session_id=self.session_id, keyword_id=self.keyword_id).process()

        SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED,
                                               details=f'{SessionType.APP_RANK_PROCESSOR} has completed')
