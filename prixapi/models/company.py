from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50)
    employee = models.ForeignKey(
        "Employee", null=True, on_delete=models.CASCADE, related_name="owner")

    class Meta:
        verbose_name = ("Company")
        verbose_name_plural = ("Companies")

    def __str__(self):
        return self.name
