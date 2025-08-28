from ..models import Exam, ExamAccessToken
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from ..exceptions import TokenNotFound, TokenAlreadyUsedError, TokeExpiredError
from django.db import transaction

class ExamService:
    @staticmethod
    def generate_token(exam_id, student_id, valid_minutes):
        try:
            student = User.objects.get(id=student_id)
            exam = Exam.objects.get(id=exam_id)
        except User.DoesNotExist:
            raise ValueError("Invalid student")
        except Exam.DoesNotExist:
            raise ValueError("Invalid exam")
        
        now = timezone.now()
        if exam.end_time < now:
            raise ValueError("Exam is already Ended")
        
        if now + timezone.timedelta(minutes=valid_minutes) > exam.end_time:
            raise ValueError("Token valid minute must not excceed exam end time")
        
        if ExamAccessToken.objects.filter(student=student, exam=exam).exists():
            raise ValueError("Token already exists for this student and exam")
        
        token = secrets.token_urlsafe(16)

        ExamAccessToken.objects.create(
            exam = exam,
            student = student,
            token = token,
            valid_from = now,
            valid_until = now + timezone.timedelta(minutes=valid_minutes)
        )

        return token, student
    
    @staticmethod
    def token_related_validation(token):
        with transaction.atomic():
            if not ExamAccessToken.objects.filter(token=token).exists():
                raise TokenNotFound("Token doesn't exist")
            
            examAccessTokenObject = ExamAccessToken.objects.select_related("exam", "student").get(token=token)
            now = timezone.now()
            if examAccessTokenObject.is_used:
                raise TokenAlreadyUsedError("Token is already used")
            if not examAccessTokenObject.valid_from <= now < examAccessTokenObject.valid_until:
                raise TokeExpiredError("Token is expired")
            
            examAccessTokenObject.is_used = True
            examAccessTokenObject.save(update_fields=['is_used'])
            return True, examAccessTokenObject

