import datetime
from collections import OrderedDict, defaultdict
from decimal import Decimal  # Import Decimal for explicit type conversions
from ..models import Transaction, TransactionType, UserProfile


class TransactionsByWeekService:
    """
    Service class for handling operations related to Transactions within a specific week.
    """

    def get_transactions_by_week(self, user_id):
        """
        Retrieves transactions for a specific user categorized by day within the current week.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            list: A list of dictionaries detailing transactions summed by day for the current week.
        """
        # Validate that the user profile exists
        user_profile = UserProfile.objects.get(user_id=user_id)

        # Define the start of the current week
        today = datetime.date.today()
        start_week = today - datetime.timedelta(today.weekday())

        # Fetch user transactions from the start of the current week up to today
        transactions = Transaction.objects.filter(
            owner=user_profile, date__range=[start_week, today]
        )

        # Aggregate transactions by day
        transactions_by_day = defaultdict(
            lambda: {"income": Decimal("0.00"), "outcome": Decimal("0.00")}
        )
        for trans in transactions:
            day_name = trans.date.strftime("%A")
            transaction_type = (
                "income" if trans.type == TransactionType.INCOME else "outcome"
            )
            transactions_by_day[day_name][transaction_type] += Decimal(trans.amount)

        # Sort the transactions by day of the week to maintain the order: Mon, Tue, Wed, etc.
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        sorted_transactions = OrderedDict(
            sorted(transactions_by_day.items(), key=lambda x: days_order.index(x[0]))
        )

        # Convert the sorted transactions to a regular list for serialization
        return [
            {"day": day, "income": data["income"], "outcome": data["outcome"]}
            for day, data in sorted_transactions.items()
            if day in days_order[: today.weekday() + 1]
        ]
