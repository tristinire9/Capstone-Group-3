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
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Component(models.Model):
    software_release = models.ForeignKey(SoftwareRelease, on_delete=models.CASCADE)
    component_name = models.CharField(max_length=200)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.component_name
