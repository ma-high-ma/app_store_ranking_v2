from app_store_ranking_v2.celery import app as celery_app
from app_store_ranking_v2.task_names import SCRAPE_AND_PROCESS_APP_RANKS
from apps.app_rank.models import ErrorLog
from apps.app_rank.services.brain import Brain


@celery_app.task(name=SCRAPE_AND_PROCESS_APP_RANKS)
def scrape_and_process_app_ranks(keyword):
    print('SCRAPE_AND_PROCESS_APP_RANKS started')
    try:
        Brain().cron_logic(keyword)
    except Exception as e:
        ErrorLog.objects.create(
            error_message=str(e),
            session_id=-1
        )

    print('SCRAPE_AND_PROCESS_APP_RANKS complete!')
