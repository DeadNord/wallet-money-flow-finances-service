from django.db import models
from django.contrib.postgres.fields import ArrayField


# Enum for transaction types to ensure that only valid transaction types are used.
class TransactionType(models.TextChoices):
    INCOME = "Income", "Income"  # Represents an income transaction.
    EXPENSE = "Expense", "Expense"  # Represents an expense transaction.


# Represents a category for transactions.
class Category(models.Model):
    name = models.CharField(max_length=255)  # The name of the category.

    def __str__(self):
        # String representation of the Category model.
        return self.name


# Represents a user's profile in the finance application.
class UserProfile(models.Model):
    user_id = models.CharField(
        primary_key=True, max_length=50
    )  # Unique identifier for the user.
    budget_limit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )  # The user's budget limit.

    def __str__(self):
        # String representation of the UserProfile model.
        return f"UserProfile {self.user_id}"


# Represents a financial transaction in the system.
class Transaction(models.Model):
    owner = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="transactions",  # Establishes a reverse relationship from UserProfile to Transaction.
        help_text="The user profile that owns this transaction.",
    )
    name = models.CharField(
        max_length=255, help_text="The name or description of the transaction."
    )
    date = models.DateField(help_text="The date when the transaction occurred.")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="The amount of the transaction."
    )
    type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
        help_text="The type of the transaction, either Income or Expense.",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        help_text="The category this transaction belongs to.",
    )
    from_account = models.CharField(
        max_length=255, help_text="The account from which the transaction was made."
    )
    note = models.TextField(
        blank=True, null=True, help_text="Additional notes about the transaction."
    )

    def __str__(self):
        # String representation of the Transaction model.
        return self.name
