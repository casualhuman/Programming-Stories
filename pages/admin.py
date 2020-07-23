from django.contrib import admin
from .models import ReportProblem

@admin.register(ReportProblem)
class ReportProblemAdmin(admin.ModelAdmin):
    list_display = ('problem', 'date_reported')