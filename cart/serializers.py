from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    size = serializers.CharField(source="variant.size.name", read_only=True)
    color = serializers.CharField(source="variant.color.name", read_only=True)
    total = serializers.SerializerMethodField()

    unit_price = serializers.SerializerMethodField()
    unit_price_promo = serializers.SerializerMethodField()

    def get_unit_price(self, obj):
        return obj.product.price
    
    def get_unit_price_promo(self, obj):
        return obj.product.get_current_price()

    def get_total(self, obj):
        return obj.get_total()
    
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "variant",
            "size",
            "color",
            "quantity",
            "unit_price",
            "unit_price_promo",
            "total",
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.get_total()
    
    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total"
        ]