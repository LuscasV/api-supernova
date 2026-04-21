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

    current_price = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    def get_current_price(self, obj):
        return obj.get_current_price()
    
    def get_is_on_sale(self, obj):
        return obj.get_current_price() != obj.price
    
    def get_discount_percentage(self, obj): 
        if obj.price > 0 and obj.get_current_price() < obj.price:
            return round(100 - (obj.get_current_price() / obj.price * 100))
        return 0
    

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "current_price",
            "is_on_sale",
            "discount_percentage",
            "gender",
            "category",
            "images",
            "variants",
            "is_featured",
            "created_at",
        ]


