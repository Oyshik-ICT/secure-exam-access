from django.contrib import admin
from .models import Exam, ExamAccessToken
from .forms import ExamAdminForm

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm
    list_display = ('title', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('title',)

admin.site.register(ExamAccessToken)