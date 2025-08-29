import logging
import secrets

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from ..exceptions import TokeExpiredError, TokenAlreadyUsedError, TokenNotFound
from ..models import Exam, ExamAccessToken

logger = logging.getLogger(__name__)


class ExamService:
    """
    Service layer for handling exam token generation and validation
    """

    @staticmethod
    def generate_token(exam_id, student_id, valid_minutes):
        """
        Generate a unique exam access token for a student
        """
        try:
            student = User.objects.get(id=student_id)
            exam = Exam.objects.get(id=exam_id)

            now = timezone.now()
            if exam.end_time < now:
                raise ValueError("Exam is already Ended")

            if now + timezone.timedelta(minutes=valid_minutes) > exam.end_time:
                raise ValueError("Token valid minute must not excceed exam end time")

            if ExamAccessToken.objects.filter(student=student, exam=exam).exists():
                raise ValueError("Token already exists for this student and exam")

            token = secrets.token_urlsafe(16)

            ExamAccessToken.objects.create(
                exam=exam,
                student=student,
                token=token,
                valid_from=now,
                valid_until=now + timezone.timedelta(minutes=valid_minutes),
            )

            return token, student

        except User.DoesNotExist:
            logger.error(f"Invalid student id: {student_id}=>{e}", exc_info=True)
            raise ValueError("Invalid student")
        except Exam.DoesNotExist:
            logger.error(f"Invalid exam id: {exam_id}=>{e}", exc_info=True)
            raise ValueError("Invalid exam")
        except Exception as e:
            logger.error(f"Unexpected error in generating token=>{e}", exc_info=True)
            raise

    @staticmethod
    def token_related_validation(token):
        """
        Validate an access exam token:
        - Must exist
        - Not already used
        - Not expired
        Marks the token as used after validation
        """
        try:
            with transaction.atomic():
                if not ExamAccessToken.objects.filter(token=token).exists():
                    raise TokenNotFound("Token doesn't exist")

                examAccessTokenObject = ExamAccessToken.objects.select_related(
                    "exam", "student"
                ).get(token=token)
                now = timezone.now()
                if examAccessTokenObject.is_used:
                    raise TokenAlreadyUsedError("Token is already used")
                if (
                    not examAccessTokenObject.valid_from
                    <= now
                    < examAccessTokenObject.valid_until
                ):
                    raise TokeExpiredError("Token is expired")

                examAccessTokenObject.is_used = True
                examAccessTokenObject.save(update_fields=["is_used"])
                return True, examAccessTokenObject
        except Exception as e:
            logger.error(
                f"Unexpected error in token_related_validation, token: {token}=>{e}",
                exc_info=True,
            )
            raise
