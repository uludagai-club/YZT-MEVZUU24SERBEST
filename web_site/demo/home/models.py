from django.db import models
from home.utils import savePdf

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents')

    def __str__(self):
        return self.name
