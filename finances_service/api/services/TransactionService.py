# services.py
from ..models import Transaction, UserProfile
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from ..serializers import TransactionSerializer


class TransactionService:
    def get_user_transactions(self, user_id, name=None, start_date=None, end_date=None):
        transactions_query = Q(owner__user__id=user_id)

        if name:
            transactions_query &= Q(name__icontains=name)
        if start_date and end_date:
            transactions_query &= Q(date__range=[start_date, end_date])

        transactions = Transaction.objects.filter(transactions_query)
        return transactions

    def delete_transaction(self, user_id, transaction_id):

        user_profile = UserProfile.objects.get(user__id=user_id)
        transaction = Transaction.objects.get(id=transaction_id, owner=user_profile)
        transaction.delete()

    def add_transaction(self, user_id, transaction_data):
        # Получаем профиль пользователя
        user_profile = UserProfile.objects.get(user__id=user_id)

        # Добавляем id владельца к данным транзакции
        transaction_data["owner"] = user_profile.id

        # Создаем и возвращаем транзакцию
        serializer = TransactionSerializer(data=transaction_data)
        if serializer.is_valid(raise_exception=True):
            return serializer.save(), None
        return None, serializer.errors
