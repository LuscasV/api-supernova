from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import OrderCreateSerializer, OrderSerializer
from .models import Order
from products.models import ProductVariant

class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        response_serializer = OrderSerializer(order)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class MyOrdersListView(ListAPIView): #LISTAPI LISTA OS OBJETOS
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # FILTRA PARA APENAS PEDIDOS DO USUARIO
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# CANCELAR ORDER
class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"detail":"Pedido não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        if order.status in ["shipped", "delivered"]:
            return Response(
                {"detail":"Este pedido não pode mais ser cancelado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if order.status == "canceled":
            return Response(
                {"detail": "Pedido já cancelado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic(): # Segurança total
            # DEVOLVER ESTOQUE
            for item in order.items.all():

                try:
                    variant = item.variant
                    variant.stock += item.quantity
                    variant.save()
                except ProductVariant.DoesNotExist:
                    pass 

            # CANCELAR PEDIDO   
            order.status = "canceled"
            order.save()

        return Response(
            {"detail": "Pedido cancelado com sucesso."},
            status=status.HTTP_200_OK
        )