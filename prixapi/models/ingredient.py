from django.db import models
from .measurement_type import MeasurementType
from .ingredient_category import IngredientCategory


class Ingredient(models.Model):

    ingredient_category = models.ForeignKey(
        IngredientCategory, on_delete=models.CASCADE)
    measurement_type = models.ForeignKey(
        MeasurementType, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    purchase_price = models.FloatField()
    purchase_quantity = models.FloatField()

    class Meta:
        verbose_name = ("Ingredient")
        verbose_name_plural = ("Ingredients")

    def __str__(self):
        return self.name
