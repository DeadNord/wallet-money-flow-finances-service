from django.utils import timezone
from ..models import Transaction, UserProfile, TransactionType
from django.db.models import Sum

class BudgetService:
    def get_user_budget(self, user_id):
        user_profile = UserProfile.objects.get(user__id=user_id)  # Репозиторий может быть вызван здесь, если нужна дополнительная абстракция
        today = timezone.now().date()
        total_expenses = Transaction.objects.filter(
            owner=user_profile,
            type=TransactionType.OUTCOME,
            date__year=today.year,
            date__month=today.month
        ).aggregate(total=Sum('amount'))['total'] or 0.00
        return {
            'budgetLimit': user_profile.budget_limit,
            'monthlyExpenses': total_expenses
        }
    