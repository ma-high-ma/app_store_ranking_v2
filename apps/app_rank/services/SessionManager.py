import shortuuid

from apps.app_rank.constants import SessionStatus
from apps.app_rank.exceptions import SessionIDDoesNotExist
from apps.app_rank.models import Session
from apps.app_rank.models.error_log import ErrorLog


class SessionManagerService:
    @staticmethod
    def create_session_id(session_type):
        uuid = shortuuid.ShortUUID().random(length=10)
        return f'{session_type}-{uuid}'

    @staticmethod
    def create_session(session_type):
        session_uuid = SessionManagerService.create_session_id(session_type)
        session = Session.objects.create(
            session_uuid=session_uuid,
            status=SessionStatus.NOT_STARTED
        )
        return session.id

    @staticmethod
    def __update_session_status(session_id, status, details):
        session_obj = Session.objects.filter(
            id=session_id
        ).first()
        if session_obj is None:
            raise SessionIDDoesNotExist
        if details is not None:
            session_obj.details = details
        session_obj.status = status
        session_obj.save()

    def update_session(self, session_id, status, details=None):
        try:
            self.__update_session_status(session_id=session_id, status=status, details=details)
        except SessionIDDoesNotExist as e:
            ErrorLog.objects.create(
                error_message=str(e),
                session_id=session_id
            )

    def process_failed_session(self, session_id, error_message):
        self.update_session(session_id, SessionStatus.FAILED, details=error_message)
        ErrorLog.objects.create(
            error_message=error_message,
            session_id=session_id
        )
