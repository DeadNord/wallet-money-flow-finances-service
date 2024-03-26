from rest_framework import serializers
from .models import Transaction, Category, UserProfile


class TransactionSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), write_only=True, source="owner"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "owner_id",
            "name",
            "date",
            "amount",
            "type",
            "category_name",
            "category_id",
            "from_account",
            "note",
        ]
        depth = 1

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def create(self, validated_data):
        owner = validated_data.get("owner")
        category = validated_data.get("category")
        if owner:
            validated_data["owner"] = owner
        if category:
            validated_data["category"] = category
        return Transaction.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user_id", "budget_limit"]
