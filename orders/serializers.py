from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product, ProductVariant
from accounts.models import Address
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

# =========================
# ITEM DO PEDIDO (RETORNO)
# =========================
class OrderItemSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source="variant.size.name", read_only=True)
    color = serializers.CharField(source="variant.color.name", read_only=True)
    
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "variant",
            "size",
            "color",
            "quantity",
            "price",
            
        ]

# =========================
# PEDIDO (RETORNO)
# =========================

class OrderSerializer(serializers.ModelSerializer):
    estimated_delivery = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True)
    payment_method = serializers.CharField(source="get_payment_method_display", read_only=True)

    def get_estimated_delivery(self, obj):
        if obj.status == "pending":
            return "Aguardando processamento"
        
        elif obj.status == "paid":
            # ainda n foi enviado
            return "Preparando envio"
        
        elif obj.status == "shipped":
            delivery_date = obj.status_updated_at + timedelta(days=1)
            remaining = delivery_date - timezone.now()

            if remaining.total_seconds() <= 0:
                return "Saiu para entrega"
            
            minutes = int(remaining.total_seconds() // 60)

            if minutes <= 1:
                return "Entrega iminente"
            
            if minutes < 60:
                return f"Entrega em aproximadamente {minutes} minutos"
            
            hours = minutes // 60
            return f"Entrega em aproximadamente {hours} horas"
        
        elif obj.status == "delivered":
            return "Pedido entregue"
        
        elif obj.status == "canceled":
            return "Pedido cancelado"

        return "Não foi possivel calcular a entrega"

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "payment_method",
            "total",
            "created_at",
            "estimated_delivery",

            # ENDEREÇO DO PEDIDO
            "street",
            "number",
            "neighborhood",
            "city",
            "state",
            "zip_code",

            "items",
        ]

# =========================
# CRIAR ITEM
# =========================
class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    variant_id = serializers.IntegerField()

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
        
        with transaction.atomic(): # Garante consistencia
        
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
                    variant = ProductVariant.objects.select_related("product").get(id=item["variant_id"])
                except ProductVariant.DoesNotExist:
                    raise serializers.ValidationError("Variação inválida.")
            
                product = variant.product
                quantity = item["quantity"]
            
                # VALIDAR ESTOQUE
                if variant.stock < quantity:
                    raise serializers.ValidationError(
                        f"Estoque insuficiente para {product.name}"
                    )
            
                # SUBTRAIR ESTOQUE
                variant.stock -= quantity
                variant.save()

                # CRIRAR ITEM
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    variant=variant
                )

                total += product.price * quantity

        order.total = total
        order.save()

        return order