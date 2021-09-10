from django.db import models

class WorkGenre(models.Model):
    work = models.ForeignKey("Work", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)