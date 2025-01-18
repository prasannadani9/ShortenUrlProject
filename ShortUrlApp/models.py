from django.db import models
from django.utils import timezone
from datetime import timedelta

class UrlDataMainModel(models.Model):
    id = models.AutoField(primary_key=True)
    main_url = models.CharField(max_length=255, null = False)
    short_url = models.CharField(max_length=150, unique=True, null=False)
    expiry_time = models.DateTimeField(null=False)
    creation_time = models.DateTimeField(null=False)

class AccessLogs(models.Model):
    id = models.AutoField(primary_key=True)
    short_url = models.ForeignKey(UrlDataMainModel, related_name='access_logs', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length = 50, null= False)
    timestamp = models.DateTimeField(null=False)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now() + timedelta(hours=5, minutes=30)
        super(AccessLogs, self).save(*args, **kwargs)