from django.db import models


class MeasurementType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = ("Measurement Type")
        verbose_name_plural = ("Measurement Types")

    def __str__(self):
        return self.name
