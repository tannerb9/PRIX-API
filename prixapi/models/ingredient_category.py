from django.db import models


class IngredientCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Ingredient Category")
        verbose_name_plural = ("Ingredient Categories")

    def __str__(self):
        return self.name
