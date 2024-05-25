from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Destination(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    http_method = models.CharField(max_length=255)
    headers = models.JSONField()