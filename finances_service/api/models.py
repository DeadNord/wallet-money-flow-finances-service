from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Enum for transaction types
class TransactionType(models.TextChoices):
    INCOME = "Income", "Income"
    OUTCOME = "Outcome", "Outcome"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"UserProfile {self.id}"


class Transaction(models.Model):
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="transactions"
    )
    name = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TransactionType.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    from_account = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
