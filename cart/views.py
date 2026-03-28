from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db import transaction

from .models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from accounts.models import Address
from .serializers import CartSerializer
from products.models import ProductVariant

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        address_id = request.data.get("address_id")

        if not address_id:
            return Response({"error": "address_id é obrigatório"}, status=400)

        #validar endereço
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({"error": "Endereço inválido"}, status=400)
        
        # Pegar carrinho
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Carrinho vazio"}, status=400)
        
        items = cart.items.select_related("variant__product").select_for_update()

        if not items.exists():
            return Response({"error": "Carrinho vazio"}, status=400)
        try:
            with transaction.atomic():
                # Criar pedido
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
            
                for item in items:
                    variant = item.variant
                    product = variant.product
                    quantity = item.quantity

                # validar estoque
                    if variant.stock < quantity:
                        raise ValidationError(f"Estoque insuficiente para {product.name}")

                    # baixar estoque
                    variant.stock -= quantity
                    variant.save()

                    # criar item do pedido
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        variant=variant,
                        quantity=quantity,
                        price=product.price
                    )

                    total += product.price * quantity

                order.total = total
                order.save()

                # limpar carrinho
                items.delete()

        except ValidationError as e:
            return Response({"error": e.detail}, status=400)

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    

# =========================
# VER CARRINHO
# =========================
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# =========================
# VER CARRINHO
# =========================
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        variant_id = request.data.get("variant_id")

        if not variant_id:
            return Response({"error": "variant_id é obrigatório"}, status=400)
        
        try:
            quantity = int(request.data.get("quantity", 1))

            if quantity <= 0:
                return Response({"error": "Quantidade deve ser maior que 0"}, status=400)
            
        except (TypeError, ValueError):
            return Response({"error": "Quantidade inválida"}, status=400)
        try:
            variant = ProductVariant.objects.select_related("product").get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error": "Variação inválida"}, status=400)
        
        # validar estoque
        if variant.stock < quantity:
            return Response({"error": "Estoque insuficiente"}, status=400)
        
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={
                "product": variant.product,
                "quantity": quantity
            }
        )

        if not created:
            new_quantity = item.quantity + quantity

            if variant.stock < new_quantity:
                return Response({"error": "Estoque insuficiente"}, status=400)

            item.quantity = new_quantity
            item.save()
        
        return Response({"message": "Produto adicionado ao carrinho"}, status=201)

# =========================
# ATUALIZAR QUANTIDADE
# =========================

class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item não encontrado"}, status=404)
        
        try:
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response({"error": "Quantidade inválida"}, status=400)

        if quantity <= 0:
            item.delete()
            return Response({"message": "item removido"})
        
        if item.variant.stock < quantity:
            return Response({"error": "Estoque insuficiente"}, status=400)
        
        item.quantity = quantity
        item.save()

        return Response({"message": "Quantidade atualizada"})

# =========================
# REMOVER ITEM
# =========================

class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item não encontrado"}, status=404)
        
        item.delete()
        return Response({"message": "Item removido"})
    
# =========================
# LIMPAR CARRINHO
# =========================
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()

        return Response({"message": "Carrinho limpo"})