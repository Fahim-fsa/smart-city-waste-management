from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('report_update', 'Report Update'),
        ('task_assignment', 'Task Assignment'),
        ('emergency_alert', 'Emergency Alert'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.user.name}"

    class Meta:
        ordering = ['-created_at']
