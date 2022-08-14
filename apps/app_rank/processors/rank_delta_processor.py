from apps.app_rank.constants import SessionStatus
from apps.app_rank.exceptions import NoPreviousAppRankForGivenKeyword
from apps.app_rank.models import AppRank, Session, ShopifyApp, RankDelta
from apps.app_rank.services.SessionManager import SessionManagerService


class RankDeltaProcessor:
    def __init__(self, session_id, keyword_id):
        self.session_id = session_id
        self.keyword_id = keyword_id
        self.rank_delta_objs = []

    def __process(self):
        print('inside __process')
        # All sessions in AppRank table will be related to HTML Processor
        session_ids_for_given_keyword = AppRank.objects.filter(keyword_id=self.keyword_id).values_list(
            'session_id', flat=True).distinct()
        print(session_ids_for_given_keyword)
        session_qs = Session.objects.filter(id__in=session_ids_for_given_keyword,
                                            status=SessionStatus.COMPLETED).order_by('-created_at')
        print(session_qs)
        if len(session_qs) <= 1:
            raise NoPreviousAppRankForGivenKeyword(keyword=self.keyword_id)

        apps_scraped_in_prev_session = AppRank.objects.filter(keyword_id=self.keyword_id, session_id=session_qs[1].id)
        apps_scraped_in_current_session = AppRank.objects.filter(keyword=self.keyword_id, session_id=session_qs[0].id)
        print(apps_scraped_in_current_session)
        print(apps_scraped_in_prev_session)
        for previously_scraped_app in apps_scraped_in_prev_session:

            current_scraped_app = apps_scraped_in_current_session.filter(
                shopify_app_id=previously_scraped_app.shopify_app_id).first()

            if not current_scraped_app:
                shopify_app = ShopifyApp.objects.get(id=previously_scraped_app.shopify_app_id)
                current_scraped_app = AppRank.objects.create(
                    shopify_app=shopify_app,
                    keyword_id=self.keyword_id,
                    rank=9999,
                    session_id_id=self.session_id
                )
                print(current_scraped_app)
            if current_scraped_app.rank != previously_scraped_app.rank:
                rank_delta_obj = RankDelta(
                    shopify_app_id=current_scraped_app.shopify_app_id,
                    prev_rank=previously_scraped_app.rank,
                    new_rank=current_scraped_app.rank,
                    rank_delta=(current_scraped_app.rank - previously_scraped_app.rank),
                    session_id=self.session_id
                )
                print(rank_delta_obj)
                self.rank_delta_objs.append(rank_delta_obj)

    def process(self):
        print('inside rank delta process func')
        SessionManagerService().update_session(self.session_id, SessionStatus.IN_PROGRESS)
        try:
            print('inside try')
            self.__process()
        except (NoPreviousAppRankForGivenKeyword, Exception) as e:
            error_msg = {
                'Exception': str(e),
                'keyword_id': self.keyword_id,
                'details': f'Error occurred during rank delta processing'
            }
            SessionManagerService().process_failed_session(self.session_id, error_msg)
            return
        RankDelta.objects.bulk_create(self.rank_delta_objs)
        SessionManagerService().update_session(self.session_id, SessionStatus.COMPLETED)
