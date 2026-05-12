from django.db import models
from django.conf import settings
from citizen_reports_app.models import WasteReport


class VolunteerTask(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    report = models.ForeignKey(WasteReport, on_delete=models.CASCADE, related_name='tasks')
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    assigned_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    notes = models.TextField(blank=True)
    before_cleanup_image = models.ImageField(upload_to='tasks/before/', blank=True, null=True)
    after_cleanup_image = models.ImageField(upload_to='tasks/after/', blank=True, null=True)

    def __str__(self):
        return f"Task for {self.report.title} - {self.volunteer.name}"

    class Meta:
        ordering = ['-assigned_date']
