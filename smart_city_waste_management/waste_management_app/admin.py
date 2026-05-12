from django.contrib import admin
from .models import VolunteerTask


@admin.register(VolunteerTask)
class VolunteerTaskAdmin(admin.ModelAdmin):
    list_display = ('report', 'volunteer', 'status', 'assigned_date', 'completion_date')
    list_filter = ('status',)
    search_fields = ('report__title', 'volunteer__name')
