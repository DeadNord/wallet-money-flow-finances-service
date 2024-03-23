from rest_framework import serializers
from .models import Transaction, Category, UserProfile


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "name",
            "date",
            "amount",
            "type",
            "category_name",
            "from_account",
            "note",
        ]

    def create(self, validated_data):
        # Преобразование имени категории в объект Category
        category_name = validated_data.pop("category_name")
        category, _ = Category.objects.get_or_create(name=category_name)
        transaction = Transaction.objects.create(**validated_data, category=category)
        return transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "budget_limit"]
