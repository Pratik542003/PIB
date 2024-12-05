from django.db import models
import datetime

# Create your models here.
class PibVideo(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField()
    date = models.DateField(default=datetime.date.today)  # Sets  to current date
    description = models.TextField()
    status = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')  # Adjust the upload_to path as needed
    video = models.FileField(upload_to='videos/')
