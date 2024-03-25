from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User
from ..models import Transaction, UserProfile, TransactionType


class UserProfileService:
    def create_user_profile(self, user_id):
        # Получаем пользователя по ID
        user = User.objects.get(id=user_id)
        # Создаем и возвращаем UserProfile
        UserProfile.objects.create(user=user)

    def get_user_budget(self, user_id):
        user_profile = UserProfile.objects.get(
            user__id=user_id
        )  # Репозиторий может быть вызван здесь, если нужна дополнительная абстракция
        today = timezone.now().date()
        total_expenses = (
            Transaction.objects.filter(
                owner=user_profile,
                type=TransactionType.OUTCOME,
                date__year=today.year,
                date__month=today.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0.00
        )
        return {
            "budgetLimit": user_profile.budget_limit,
            "monthlyExpenses": total_expenses,
        }