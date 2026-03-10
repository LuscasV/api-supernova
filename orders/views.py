from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer, OrderSerializer
from .models import Order

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