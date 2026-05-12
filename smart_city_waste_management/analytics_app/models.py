from django.db import models


class AnalyticsReport(models.Model):
    area_name = models.CharField(max_length=200)
    total_reports = models.IntegerField(default=0)
    completed_reports = models.IntegerField(default=0)
    pending_reports = models.IntegerField(default=0)
    active_volunteers = models.IntegerField(default=0)
    generated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Analytics - {self.area_name} ({self.generated_date})"

    class Meta:
        ordering = ['-generated_date']
