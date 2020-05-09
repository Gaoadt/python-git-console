from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=2000)
