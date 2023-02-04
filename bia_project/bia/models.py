from django.db import models

class Bia(models.Model):
    active_energy = models.FloatField()
    meter_date = models.DateTimeField()
    meter_id = models.IntegerField()


