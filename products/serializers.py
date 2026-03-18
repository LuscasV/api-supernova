from rest_framework import serializers
from .models import (
    Gender,
    Category,
    Product,
    Size,
    Color,
    ProductImage,
    ProductVariant,
)


# =========================
# GENDER
# =========================
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ["id", "name", "slug"]


# =========================
# CATEGORY (com hierarquia)
# =========================
class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "children"]

    def get_children(self, obj):
        return [
            {
                "id": child.id,
                "name": child.name,
                "slug": child.slug,
            }
            for child in obj.subcategories.all()
        ]


# =========================
# SIZE
# =========================
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "name"]


# =========================
# COLOR
# =========================
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["id", "name", "hex_code"]

# =========================
# PRODUCT IMAGE
# =========================
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main"]


class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "size",
            "color",
            "stock"
        ]

# =========================
# PRODUCT (principal)
# =========================
class ProductSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "gender",
            "category",
            "images",
            "variants",
            "is_featured",
            "created_at",
        ]


