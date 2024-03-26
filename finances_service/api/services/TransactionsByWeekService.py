# services.py
import datetime
from collections import defaultdict
from ..models import Transaction, UserProfile, TransactionType


class TransactionsByWeekService:
    def get_transactions_by_week(self, user_id):
        user_profile = UserProfile.objects.get(user_id=user_id)

        # Получаем начало и конец текущей недели
        today = datetime.date.today()
        start_week = today - datetime.timedelta(today.weekday())
        end_week = start_week + datetime.timedelta(7)

        # Извлекаем транзакции пользователя за текущую неделю
        transactions = Transaction.objects.filter(
            owner=user_profile, date__range=[start_week, end_week]
        )

        # Сортируем и суммируем транзакции по дням недели
        transactions_by_day = defaultdict(lambda: {"income": 0.00, "outcome": 0.00})
        for trans in transactions:
            day_name = trans.date.strftime("%A")
            if trans.type == TransactionType.INCOME:
                transactions_by_day[day_name]["income"] += trans.amount
            else:
                transactions_by_day[day_name]["outcome"] += trans.amount

        # Преобразуем в список для ответа
        result = [
            {"name": day, "income": data["income"], "outcome": data["outcome"]}
            for day, data in transactions_by_day.items()
        ]
        return result
