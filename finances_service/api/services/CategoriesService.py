from ..models import Category


class CategoriesService:
    def get_all_categories(self):
        categories = Category.objects.all().order_by(
            "name"
        )  # Получаем все категории, отсортированные по имени
        return [
            {"id": category.id, "name": category.name} for category in categories
        ]  # Возвращаем список словарей
