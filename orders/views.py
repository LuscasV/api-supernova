from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderCreateSerializer, OrderSerializer
from .models import Order

class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

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