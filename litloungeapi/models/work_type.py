from django.db import models

class WorkType(models.Model):
    label = models.CharField(max_length=50)