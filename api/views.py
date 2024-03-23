from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import views, status
from rest_framework.response import Response
from .models import UserProfile, Transaction, TransactionType
from .serializers import UserProfileSerializer, TransactionSerializer
from django.db.models import Sum
from .services import (
    BudgetService,
    TransactionService,
    ExpensesByCategoriesService,
    TransactionsByWeekService,
)


class BudgetView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        budget_service = BudgetService()
        try:
            data = budget_service.get_user_budget(user_id)
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TransactionsView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        name = request.query_params.get("name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction_service = TransactionService()
        transactions = transaction_service.get_user_transactions(
            user_id, name, start_date, end_date
        )
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpensesByCategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        service = ExpensesByCategoriesService()
        expenses_data = service.get_expenses_by_categories(user_id)
        if expenses_data is None:
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(expenses_data, status=status.HTTP_200_OK)


class TransactionsByWeekView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        transactions_by_week_service = TransactionsByWeekService()
        try:
            data = transactions_by_week_service.get_transactions_by_week(user_id)
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AddTransactionView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction_service = TransactionService()

        try:
            transaction, errors = transaction_service.add_transaction(
                user_id, request.data
            )
            if transaction:
                return Response(
                    TransactionSerializer(transaction).data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DeleteTransactionView(APIView):
    def delete(self, request, id, *args, **kwargs):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction_service = TransactionService()
        transaction = transaction_service.delete_transaction(user_id, id)
        if transaction is None:
            return Response(
                {"error": "Transaction does not exist or you do not have permission"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "Transaction deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
