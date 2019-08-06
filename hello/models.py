from django.db import models

# Create your models here.
# class Greeting(models.Model):
#     when = models.DateTimeField("date created", auto_now_add=True)

class Component(models.Model):
    name = models.CharField(max_length=255)
    version_number = models.CharField(max_length=10)
    date = models.CharField(max_length=12)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = "temp_user"
