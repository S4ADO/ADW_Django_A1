from django.db import models
from django.conf import settings

# Create your models here.

class Task(models.Model):
	title = models.CharField(max_length=255)
	body = models.CharField(max_length=5000)
	created_at = models.DateTimeField()
	completed_at = models.DateTimeField()
	complete = models.IntegerField(default=0)
	userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)