from django.contrib import admin
from .models import WasteReport


@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'citizen', 'location', 'status', 'report_date')
    list_filter = ('status', 'report_date')
    search_fields = ('title', 'location', 'citizen__name')
    list_editable = ('status',)
