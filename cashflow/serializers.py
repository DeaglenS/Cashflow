from rest_framework import serializers
from .models import MovementType, Status, Category, Subcategory, CashFlow

class MovementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementType
        fields = ["id", "name"]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]

class CategorySerializer(serializers.ModelSerializer):
    movement_type = MovementTypeSerializer(read_only=True)
    movement_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MovementType.objects.all(), source="movement_type", write_only=True
    )
    class Meta:
        model = Category
        fields = ["id", "name", "movement_type", "movement_type_id"]

class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    class Meta:
        model = Subcategory
        fields = ["id", "name", "category", "category_id"]

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = [
            "id",
            "record_date",
            "status",
            "movement_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]

    def validate(self, attrs):
        category = attrs.get("category") or (self.instance and self.instance.category)
        subcategory = attrs.get("subcategory") or (self.instance and self.instance.subcategory)
        movement_type = attrs.get("movement_type") or (self.instance and self.instance.movement_type)

        if category and movement_type and category.movement_type_id != movement_type.id:
            raise serializers.ValidationError("Категория не относится к выбранному типу.")
        if subcategory and category and subcategory.category_id != category.id:
            raise serializers.ValidationError("Подкатегория не принадлежит выбранной категории.")
        return attrs
