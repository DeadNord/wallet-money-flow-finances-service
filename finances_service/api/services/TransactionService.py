# Application-specific imports
from ..models import Transaction, UserProfile
from ..serializers import TransactionSerializer
from django.db.models import Q


class TransactionService:
    """
    Service class for handling Transaction-related operations.
    """

    def get_user_transactions(self, user_id, name=None, start_date=None, end_date=None):
        """
        Retrieves transactions for a specific user, optionally filtered by name and date range.

        Args:
            user_id (str): The unique identifier of the user.
            name (str, optional): A name to filter the transactions by.
            start_date (date, optional): The start date for the transactions filter.
            end_date (date, optional): The end date for the transactions filter.

        Returns:
            QuerySet: A QuerySet of Transaction instances matching the criteria.
        """
        transactions_query = Q(owner__user_id=user_id)

        if name:
            transactions_query &= Q(name__icontains=name)
        if start_date and end_date:
            transactions_query &= Q(date__range=[start_date, end_date])
        return Transaction.objects.filter(transactions_query).order_by("-date")

    def delete_transaction(self, transaction_id, user_id):
        """
        Deletes a transaction for a specific user if the user is the owner of the transaction.

        Args:
            transaction_id (int): The unique identifier of the transaction to be deleted.
            user_id (str): The unique identifier of the user attempting to delete the transaction.

        """
        transaction = Transaction.objects.get(id=transaction_id, owner__user_id=user_id)
        transaction.delete()

    def add_transaction(self, user_id, transaction_data):
        """
        Adds a new transaction for a specific user.

        Args:
            user_id (str): The unique identifier of the user.
            transaction_data (dict): A dictionary containing data of the transaction.

        Returns:
            tuple: A tuple containing the Transaction instance (or None if validation fails)
            and None or a dictionary of validation errors.
        """
        UserProfile.objects.get(user_id=user_id)
        transaction_data["owner_id"] = (
            user_id  # Correctly assign the user ID to the owner_id field
        )

        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid(raise_exception=True):
            return serializer.save()  # Return transaction and None if successful
        else:
            return None, serializer.errors  # Return None and errors if validation fails
