from django.db import models
from django.utils.translation import gettext_lazy as _


class SessionStatus(models.TextChoices):
    NOT_STARTED = 'not_started', _('Not Started')
    IN_PROGRESS = 'in_progress', _('In Progress')
    COMPLETED = 'completed', _('Completed')
    FAILED = 'failed', _('Failed')
    INCOMPLETE = 'incomplete', _('Incomplete')


class ScrapedHTMLStatus(models.TextChoices):
    NOT_STARTED = 'not_started', _('Not Started')
    IN_PROGRESS = 'in_progress', _('In Progress')
    PROCESSED = 'processed', _('Processed')
    FAILED = 'failed', _('Failed')


class SessionType:
    HTML_SCRAPER = 'html-scraper'
    HTML_PROCESSOR = 'html-processor'
    RANK_DELTA_PROCESSOR = 'rank-delta-processor'
    APP_DATA_DELTA_PROCESSOR = 'app-data-delta-processor'
    ADHOC_PROCESSOR = 'adhoc-processor'


RETRY_MAX_ATTEMPTS = 3
