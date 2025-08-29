from django.contrib import admin

from .forms import ExamAdminForm
from .models import Exam, ExamAccessToken


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm
    list_display = ("title", "start_time", "end_time")
    list_filter = ("start_time", "end_time")
    search_fields = ("title",)


admin.site.register(ExamAccessToken)
