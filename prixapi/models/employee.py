from django.db import models
from django.contrib.auth.models import User
from .company import Company


class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_admin = models.BooleanField()

    class Meta:
        verbose_name = ("Employee")
        verbose_name_plural = ("Employees")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
