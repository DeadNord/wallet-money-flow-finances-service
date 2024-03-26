from django.urls import path
from . import views

urlpatterns = [
    path("budget/", views.BudgetView.as_view(), name="budget"),
    path("transactions/", views.TransactionsView.as_view(), name="transactions"),
    path(
        "categories/",
        views.CategoriesView.as_view(),
        name="categories",
    ),
    path(
        "expenses-by-categories/",
        views.ExpensesByCategoriesView.as_view(),
        name="expenses_by_categories",
    ),
    path(
        "transactions-by-week/",
        views.TransactionsByWeekView.as_view(),
        name="transactions_by_week",
    ),
    path(
        "add-transaction/", views.AddTransactionView.as_view(), name="add_transaction"
    ),
    path(
        "delete-transaction/<int:id>/",
        views.DeleteTransactionView.as_view(),
        name="delete_transaction",
    ),
    path(
        "create_user_profile/",
        views.CreateUserProfileView.as_view(),
        name="create_user_profile",
    ),
    path(
        "update-budget/",
        views.UpdateUserBudgetLimitView.as_view(),
        name="update-user-budget-limit",
    ),
]
