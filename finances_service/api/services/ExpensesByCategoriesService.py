from datetime import timezone
from collections import defaultdict
from ..models import Transaction, UserProfile, TransactionType


class ExpensesByCategoriesService:
    def get_expenses_by_categories(self, user_id):
        # Получаем профиль пользователя и проверяем его на существование

        user_profile = UserProfile.objects.get(user_id=user_id)

        # Получаем транзакции пользователя за текущий месяц
        today = timezone.now().date()
        expenses = Transaction.objects.filter(
            owner=user_profile,
            type=TransactionType.OUTCOME,
            date__year=today.year,
            date__month=today.month,
        )

        # Группируем расходы по категориям
        expenses_by_category = defaultdict(
            float
        )  # Словарь для хранения сумм расходов по категориям
        for expense in expenses:
            expenses_by_category[expense.category.name] += expense.amount

        # Генерируем оттенки фиолетового цвета
        categories_count = len(expenses_by_category)
        color_shades = self.generate_purple_shades(categories_count)

        # Формируем ответ
        response = []
        for (category, total), color in zip(expenses_by_category.items(), color_shades):
            response.append({"name": category, "value": total, "color": color})

        return response

    @staticmethod
    def generate_purple_shades(num_shades):
        max_lightness = 90
        min_lightness = 30
        shades = []
        for i in range(num_shades):
            lightness = min_lightness + (max_lightness - min_lightness) * (
                i / (num_shades - 1)
            )
            shades.append(f"hsl(270, 50%, {lightness}%)")
        return shades
