from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE
from django.contrib.auth.models import User
from .company import Company


class Employee(SafeDeleteModel):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company")
    is_admin = models.BooleanField()
    _safedelete_policy = SOFT_DELETE

    class Meta:
        verbose_name = ("Employee")
        verbose_name_plural = ("Employees")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
