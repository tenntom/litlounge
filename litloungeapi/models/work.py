from django.db import models

class Work(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=150)
    work_type = models.ForeignKey("WorkType", on_delete=models.DO_NOTHING)
    identifier = models.CharField(max_length=50)
    url_link = models.CharField(max_length=150)
    description = models.TextField()
    posted_by = models.ForeignKey("Reader", on_delete=models.CASCADE)
    genres = models.ManyToManyField("Genre", through="WorkGenre", related_name="works")

    @property
    def genre_name(self):
        return self.genre.label

