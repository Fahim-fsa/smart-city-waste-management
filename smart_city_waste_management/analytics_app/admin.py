from django.contrib import admin
from .models import AnalyticsReport


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'total_reports', 'completed_reports', 'pending_reports', 'generated_date')
