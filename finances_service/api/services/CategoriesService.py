from ..models import Category


class CategoriesService:
    """
    Service class for handling operations related to Category objects.
    """

    def get_all_categories(self):
        """
        Retrieves all categories from the database, ordered by their name.

        Returns:
            list: A list of dictionaries where each dictionary represents a category with its 'id' and 'name'.
        """
        # Fetch all category records from the database, ordering them alphabetically by name.
        categories = Category.objects.all().order_by("name")

        # Convert the queryset of Category objects into a list of dictionaries,
        # simplifying the structure for consumers of this service.
        return [{"id": category.id, "name": category.name} for category in categories]
