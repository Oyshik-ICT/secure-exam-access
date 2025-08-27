from ..models import Exam, ExamAccessToken
from django.contrib.auth.models import User
from django.utils import timezone
import secrets

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

        return token

