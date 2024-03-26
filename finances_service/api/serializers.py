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
            "category",
            "from_account",
            "note",
        ]
        depth = 1

    def create(self, validated_data):
        # Преобразование имени категории в объект Category
        return Transaction.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user_id", "budget_limit"]
