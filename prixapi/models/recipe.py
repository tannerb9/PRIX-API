from django.db import models
from .employee import Employee
from .recipe_category import RecipeCategory


class Recipe(models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    recipe_category = models.ForeignKey(
        RecipeCategory, on_delete=models.CASCADE)
    batch_sale_price = models.IntegerField()
    name = models.CharField(max_length=80)
    serving_sale_price = models.IntegerField()
    servings_per_batch = models.IntegerField()

    class Meta:
        verbose_name = ("Recipe")
        verbose_name_plural = ("Recipes")

    def __str__(self):
        return self.name
