from django.db import models

# Create your models here.

class Partner(models.Model):
    # adapter = models.ForeignKey('adapters.Adapter', related_name='rules')
    # adapter_call_name = models.CharField(max_length=100, choices=AdapterCallName.choices, default='')
    name = models.CharField(default='', max_length=300)

    # rule = models.ForeignKey('Rule', related_name='data_sets')


class Worker(models.Model):
    first_name = models.CharField(default='', max_length=300)
    last_name = models.CharField(default='', max_length=300)
    partner = models.ForeignKey('Partner', related_name='workers')
