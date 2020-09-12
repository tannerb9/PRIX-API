from django.db import models
from .measurement_type import MeasurementType
from .ingredient import Ingredient
from .recipe import Recipe


class RecipeIngredient(models.Model):

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement_type = models.ForeignKey(
        MeasurementType, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = ("Recipe Ingredient")
        verbose_name_plural = ("Recipe Ingredients")

    def __str__(self):
        return self.ingredient.name
