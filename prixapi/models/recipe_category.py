from django.db import models


class RecipeCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Recipe Category")
        verbose_name_plural = ("Recipe Categories")

    def __str__(self):
        return self.name
