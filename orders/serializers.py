from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from accounts.models import Address


# =========================
# ITEM DO PEDIDO (RETORNO)
# =========================
class OrderItemSerializer(serializers.ModelSerializer):
    
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
            "price",
            "size",
            "color",
        ]

# =========================
# PEDIDO (RETORNO)
# =========================

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "total",
            "created_at",
            "items",
        ]

# =========================
# CRIAR ITEM
# =========================
class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

# =========================
# CRIAR ITEM
# =========================
class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    items = OrderItemCreateSerializer(many=True)

    def create(self, validated_data):
        user = self.context["request"].user
        address_id = validated_data["address_id"]
        items_data = validated_data["items"]

        # VERIFICA SE O ENDEREÇO PERTENCE AO USUÁRIO
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Endereço inválido.")
        
        # CRIAR PEDIDO COPIANDO O ENDEREÇO
        order = Order.objects.create(
            user=user,
            street=address.street,
            number=address.number,
            neighborhood=address.neighborhood,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
        )

        total = 0

        # CRIAR ITENS
        for item in items_data:
            try:
                product = Product.objects.get(id=item["product_id"])
            except Product.DoesNotExist:
                raise serializers.ValidationError("Produto inválido.")
            
            quantity = item["quantity"]
            price = product.price
            size = item["size"]
            color = item["color"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                size=size,
                color=color
            )

            total += price * quantity

            order.total = total
            order.save()

        return order