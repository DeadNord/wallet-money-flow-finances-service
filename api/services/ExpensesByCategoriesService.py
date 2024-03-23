from datetime import timezone
from django.db.models import Sum
from collections import defaultdict
import random
from ..models import Transaction, UserProfile, TransactionType

class ExpensesByCategoriesService:
    def get_expenses_by_categories(self, user_id):
        # Получаем профиль пользователя и проверяем его на существование
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return None  # Можно вернуть None или поднять исключение

        # Получаем транзакции пользователя за текущий месяц
        today = timezone.now().date()
        expenses = Transaction.objects.filter(
            owner=user_profile,
            type=TransactionType.OUTCOME,
            date__year=today.year,
            date__month=today.month
        )

        # Группируем расходы по категориям
        expenses_by_category = defaultdict(float)  # Словарь для хранения сумм расходов по категориям
        for expense in expenses:
            expenses_by_category[expense.category.name] += expense.amount

        # Формируем ответ
        response = []
        for category, total in expenses_by_category.items():
            response.append({
                'name': category,
                'value': total,
                'color': f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'  # Случайный цвет для каждой категории
            })
        
        return response
