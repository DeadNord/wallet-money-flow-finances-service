# Standard library imports
# No standard library imports in this snippet.

# Third-party imports
from marshmallow import ValidationError
from drf_yasg.utils import swagger_auto_schema

# Django imports
# No specific Django imports apart from models and views which are application-specific.

# Django REST Framework imports
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


# Application-specific imports
from .models import (
    Transaction,
    UserProfile,
)  # Transaction is not used here, so it can be removed.
from .services.UserProfileService import UserProfileService
from .services.TransactionService import TransactionService
from .services.TransactionsByWeekService import TransactionsByWeekService
from .services.ExpensesByCategoriesService import ExpensesByCategoriesService
from .services.CategoriesService import CategoriesService
from .schemas.swagger_schemas import (
    add_transaction_request_body,  # Keep this if used in other classes within this file.
    transaction_query_params,  # Same as above.
    delete_transaction_params,  # Same as above.
    update_user_profile_budget_limit_schema,  # Same as above.
)
from .serializers import TransactionSerializer


# BaseView sets common properties for all API views.
class BaseView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "global"


# CreateUserProfileView handles the creation of new user profiles.
class CreateUserProfileView(BaseView):

    @swagger_auto_schema(
        security=[{"User": []}]
    )  # Swagger schema for API documentation.
    def post(self, request, *args, **kwargs):
        user_id = request.headers.get("user-id")
        # Validate that a user ID is provided.
        if not user_id:
            return Response(
                {"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_profile_service = UserProfileService()
        try:
            # Create a new UserProfile using the service layer.
            user_profile_service.create_user_profile(user_id)
            return Response(
                {"message": "UserProfile created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:  # Handle validation errors from the service layer.
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:  # General exception handler for unexpected errors.
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BudgetView(BaseView):
    """
    A view that handles requests to get the budget information for a specific user.
    Requires user ID to be provided in the request headers.
    """

    @swagger_auto_schema(
        security=[{"User": []}]
    )  # Documenting API endpoint security requirements
    def get(self, request, *args, **kwargs):
        # Extract the user ID from the request headers
        user_id = request.headers.get("user-id")

        # Validate that the user ID is provided
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Initialize the UserProfileService to retrieve user's budget information
        user_profile_service = UserProfileService()
        try:
            # Attempt to retrieve budget information using the user ID
            data = user_profile_service.get_user_budget(user_id)
            return Response(
                data, status=status.HTTP_200_OK
            )  # Successfully retrieved budget information
        except UserProfile.DoesNotExist:
            # Handle case where the UserProfile does not exist for the given user ID
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class TransactionsView(BaseView):

    @swagger_auto_schema(
        security=[{"User": []}], manual_parameters=transaction_query_params
    )
    def get(self, request, *args, **kwargs):
        user_id = request.headers.get("user-id")
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # Extract query parameters directly
            params = request.query_params
            name = params.get("name")
            start_date = params.get("start_date")
            end_date = params.get("end_date")

            # Utilize the transaction service to retrieve user transactions
            transaction_service = TransactionService()
            transactions = transaction_service.get_user_transactions(
                user_id, name, start_date, end_date
            )

            # Serialize the transaction data for the response
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            # Handle validation errors, such as incorrect dates formats
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": "An unexpected error occurred: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExpensesByCategoriesView(BaseView):
    """
    View responsible for retrieving and responding with expense data categorized by categories
    for a specific user identified by user_id. The expenses considered are only those within the current month.
    """

    @swagger_auto_schema(security=[{"User": []}])
    def get(self, request, *args, **kwargs):
        # Extract the user ID from the request headers.
        user_id = request.headers.get("user-id")

        # Ensure the user_id is provided, else return a 400 Bad Request response.
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Initialize the service to fetch expenses categorized by categories.
        service = ExpensesByCategoriesService()
        try:
            # Attempt to retrieve expenses data for the given user.
            expenses_data = service.get_expenses_by_categories(user_id)
            return Response(expenses_data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            # If the UserProfile is not found, return a 404 Not Found response.
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Handle any unexpected exceptions to prevent internal server errors.
            # Log this error as well for debugging purposes.
            # Consider logging the error here for better debuggability.
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionsByWeekView(BaseView):
    """
    View for retrieving a summary of a user's transactions grouped by day for the current week.
    """

    @swagger_auto_schema(security=[{"User": []}])
    def get(self, request, *args, **kwargs):
        # Extract the user ID from request headers
        user_id = request.headers.get("user-id")
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        transactions_by_week_service = TransactionsByWeekService()
        try:
            # Attempt to retrieve and return the transaction summary
            data = transactions_by_week_service.get_transactions_by_week(user_id)
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            # Handle case where user profile is not found
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddTransactionView(BaseView):

    @swagger_auto_schema(
        security=[{"User": []}], request_body=add_transaction_request_body
    )
    def post(self, request, *args, **kwargs):
        user_id = request.headers.get("user-id")
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Utilize the transaction service to add a new transaction
        transaction_service = TransactionService()

        try:
            transaction = transaction_service.add_transaction(user_id, request.data)
            return Response(
                TransactionSerializer(transaction).data,
                status=status.HTTP_201_CREATED,
            )
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            # Handle specific validation errors
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUserBudgetLimitView(BaseView):
    """
    View for updating the budget limit of a user's profile. This view expects a user ID
    and a new budget limit in the request. The user ID should be passed in the request headers,
    and the new budget limit should be included in the request body.
    """

    @swagger_auto_schema(
        security=[{"User": []}],
        request_body=update_user_profile_budget_limit_schema,
    )
    def patch(self, request, *args, **kwargs):
        # Extracting necessary information from the request
        user_id = request.headers.get("user-id")
        budget_limit = request.data.get("budget_limit")

        # Validating the presence of user_id and budget_limit in the request
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if budget_limit is None:
            return Response(
                {"error": "New budget limit is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Attempting to update the user's budget limit using the UserProfileService
        user_profile_service = UserProfileService()
        try:
            updated_user_profile = user_profile_service.update_user_budget_limit(
                user_id, budget_limit
            )
            return Response(
                {
                    "message": "Budget limit updated successfully",
                    "new_budget_limit": updated_user_profile.budget_limit,
                },
                status=status.HTTP_200_OK,
            )
        except UserProfile.DoesNotExist:
            # Handling the case where the user profile does not exist
            return Response(
                {"error": "UserProfile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteTransactionView(BaseView):

    @swagger_auto_schema(
        security=[{"User": []}], manual_parameters=delete_transaction_params
    )
    def delete(self, request, id, *args, **kwargs):
        user_id = request.headers.get("user-id")
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        transaction_service = TransactionService()
        try:
            transaction_service.delete_transaction(id, user_id)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": " User profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Transaction.DoesNotExist:
            return Response(
                {"error": "Transaction does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "Transaction deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CategoriesView(BaseView):
    """
    A view that handles requests for retrieving all categories available in the system.
    This view does not require any specific parameters and returns a list of all categories.
    """

    def get(self, request, *args, **kwargs):
        # Initialize the CategoriesService to retrieve category data
        categories_service = CategoriesService()

        # Fetch all categories using the service
        try:
            categories = categories_service.get_all_categories()
        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Return the list of categories with a 200 OK status
        return Response(categories, status=status.HTTP_200_OK)
