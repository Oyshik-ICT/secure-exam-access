import logging

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)



@shared_task(bind=True)
def send_token(self, token, email):
    try:
        link = f"http://127.0.0.1:8000/api/exams/access/{token}/"
        send_mail(
        subject="Exam Link",
        message=f"Click the link to give the exam: {link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )
        return "Done"

    except Exception as e:
        logger.error(f"Error in count_words: {str(e)}")
        return "Error"