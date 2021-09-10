from django.db import models

class Talk(models.Model):
    host = models.ForeignKey("Reader", on_delete=models.CASCADE)
    work = models.ForeignKey("Work", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    title = models.CharField(max_length=100)
    sup_materials = models.CharField(max_length=250)
    zoom_meeting_id = models.CharField(max_length=50)
    zoom_meeting_password = models.CharField(max_length=50)
    participants = models.ManyToManyField("Reader", through="ReaderEvent", related_name="attending")


    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joind = value