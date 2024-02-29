from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Job(models.Model):
    job_title = models.CharField(max_length=100)
    requirements = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    agency = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title



