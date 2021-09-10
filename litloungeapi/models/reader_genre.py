from django.db import models

class ReaderGenre(models.Model):
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)