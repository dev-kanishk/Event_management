from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank = False)
    date  = models.DateField()
    time  = models.TextField()
