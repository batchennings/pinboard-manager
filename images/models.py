import os
from django.db import models
from datetime import date

# Create your models here.
def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, "images")

class Image(models.Model):
    name = models.CharField(max_length=255)
    file = models.TextField()
    thumb = models.TextField(null=True)
    tags = models.TextField()
    date_created = models.DateField(default=date.today)
