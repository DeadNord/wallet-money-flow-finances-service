from decimal import Decimal
from django.utils import timezone
from collections import defaultdict
from ..models import Transaction, UserProfile, TransactionType


class ExpensesByCategoriesService:
    """
    Service for handling operations related to retrieving user expenses categorized by categories.
    """

    def get_expenses_by_categories(self, user_id):
        """
        Retrieves and aggregates expenses by categories for the user specified by user_id for the current month.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            list: A list of dictionaries with each dictionary containing details of expenses for a category.
        """
        # Ensure the user profile exists
        user_profile = UserProfile.objects.get(user_id=user_id)

        # Get today's date using the correct timezone method
        today = timezone.now().date()

        # Fetch user's expenses for the current month
        expenses = Transaction.objects.filter(
            owner=user_profile,
            type=TransactionType.EXPENSE,
            date__year=today.year,
            date__month=today.month,
        )

        # Group expenses by categories and sum their amounts
        expenses_by_category = defaultdict(lambda: Decimal("0.00"))
        for expense in expenses:
            expenses_by_category[expense.category.name] += expense.amount

        # Generate color shades for each category (for UI representation, perhaps)
        categories_count = len(expenses_by_category)
        color_shades = self.generate_purple_shades(categories_count)

        # Prepare the response data
        response = [
            {"name": category, "value": total, "color": color}
            for (category, total), color in zip(
                expenses_by_category.items(), color_shades
            )
        ]

        return response

    @staticmethod
    def generate_purple_shades(num_shades):
        """
        Generates a list of purple color shades.

        Args:
            num_shades (int): Number of shades to generate.

        Returns:
            list: A list of HSL color strings.
        """
        # Safeguard against division by zero
        if num_shades <= 1:
            return [
                "hsl(270, 50%, 60%)"
            ]  # Return a default shade or handle this case as needed

        max_lightness = 90
        min_lightness = 30
        shades = []
        for i in range(num_shades):
            lightness = min_lightness + (max_lightness - min_lightness) * (
                i / (num_shades - 1)
            )
            shades.append(f"hsl(270, 50%, {lightness}%)")
        return shades
