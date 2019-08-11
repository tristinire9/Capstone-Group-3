import datetime

from django.db import models

from django.utils import timezone


# Create your models here.
class SoftwareRelease(models.Model):
    product_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.product_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Component(models.Model):
    software_release = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE)
    component_name = models.CharField(max_length=200)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.component_name
