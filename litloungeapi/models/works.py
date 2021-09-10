from django.db import models

class Work(models.Model):
    title = models.CharField(max_length=100)
    media_type = models.ForeignKey("WorkType", on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50)
    url_link = models.CharField(max_length=150)
    description = models.TextField()
    genres = models.ManyToManyField("Genre", through="WorkGenre", related_name="work")


