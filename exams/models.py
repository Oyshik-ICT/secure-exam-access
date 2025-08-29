from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Exam(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        super().clean()
        now = timezone.now()
        if self.start_time <= now:
            raise ValidationError("Exam time must be future not past")
        if self.start_time >= self.end_time:
            raise ValidationError("Exam End time must be greater than Start time")

    def __str__(self):
        return f"Exam name: {self.title}"


class ExamAccessToken(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="ExamAccessTokens"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ExamAccessTokens"
    )
    token = models.CharField(max_length=36, unique=True)
    is_used = models.BooleanField(default=False)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("exam", "student")

    def __str__(self):
        return f"Exam name: {self.exam.title}, student: {self.student.username}"
