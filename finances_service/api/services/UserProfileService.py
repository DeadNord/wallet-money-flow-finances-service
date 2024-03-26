# Standard library imports


# Django imports
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError

# Application-specific imports
from ..models import UserProfile, Transaction, TransactionType


class UserProfileService:
    """
    Service class for handling UserProfile-related operations.
    """

    def create_user_profile(self, user_id):
        """
        Creates a new UserProfile if one with the given user_id does not exist.

        Args:
            user_id (str): The unique identifier for the user.

        Raises:
            ValidationError: If a UserProfile with the provided user_id already exists.
        """
        if UserProfile.objects.filter(user_id=user_id).exists():
            raise ValidationError("UserProfile already exists")
        return UserProfile.objects.create(user_id=user_id)

    def get_user_budget(self, user_id):
        """
        Retrieves the budget limit and total monthly expenses for the specified user.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            dict: A dictionary containing the user's budget limit and total monthly expenses.
        """
        user_profile = UserProfile.objects.get(user_id=user_id)
        today = timezone.now().date()
        total_expenses = (
            Transaction.objects.filter(
                owner=user_profile,
                type=TransactionType.EXPENSE,
                date__year=today.year,
                date__month=today.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0.00
        )
        return {
            "budgetLimit": user_profile.budget_limit,
            "monthlyExpenses": total_expenses,
        }

    def update_user_budget_limit(self, user_id, new_budget_limit):
        """
        Updates the budget limit for a specified user's UserProfile.

        Args:
            user_id (str): The unique identifier for the user.
            new_budget_limit (float): The new budget limit to set.

        Returns:
            UserProfile: The updated UserProfile instance.
        """
        user_profile = UserProfile.objects.get(user_id=user_id)
        user_profile.budget_limit = new_budget_limit
        user_profile.save()
        return user_profile
