from django.db import models

class Driver(models.Model):
    first_name = models.CharField(max_length=255)