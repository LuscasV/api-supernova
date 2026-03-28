from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    size = serializers.CharField(source="variant.size.name", read_only=True)
    color = serializers.CharField(source="variant.color.name", read_only=True)
    total = serializers.SerializerMethodField()

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
            "total"
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