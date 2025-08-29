import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_token(self, token, email):
    """
    Celery task to send exam access token via email
    """
    try:
        link = f"http://127.0.0.1:8000/api/exams/access/{token}/"
        send_mail(
            subject="Exam Link",
            message=f"Click the link to give the exam: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        logger.info(f"Exam email send successfully to {email} with token={token}")
        return "Done"

    except Exception as e:
        logger.error(
            f"Faild to send exam token email to {email}, token={token}=>{e}",
            exc_info=True,
        )
        return "Error"
