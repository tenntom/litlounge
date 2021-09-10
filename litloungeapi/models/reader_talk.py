from django.db import models

class ReaderTalk(models.Model):
    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    talk = models.ForeignKey("Talk", on_delete=models.CASCADE)