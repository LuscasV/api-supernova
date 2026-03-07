from rest_framework import serializers
from .models import (
    Gender,
    Category,
    Product,
    ProductColor,
    Size,
    Color,
    ProductImage,
    ProductSize,
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
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]

    def get_parent(self, obj):
        if obj.parent:
            return {
                "id": obj.parent.id,
                "name": obj.parent.name,
                "slug": obj.parent.slug,
            }
        return None


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
# PRODUCT SIZE (estoque)
# =========================
class ProductSizeSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = ProductSize
        fields = ["id", "size", "stock"]


# =========================
# PRODUCT IMAGE
# =========================
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main"]

class ProductColorSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = ProductColor
        fields = ["id", "color", "stock"]



# =========================
# PRODUCT (principal)
# =========================
class ProductSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)

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
            "sizes",
            "colors",
            "is_featured",
            "created_at",
        ]

