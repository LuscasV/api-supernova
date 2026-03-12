from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import Address, WishlistItem
from .serializers import RegisterSerializer, AddressSerializer, WishlistSerializer, AddWishlistSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Usuário criado com sucesso"},
            status=status.HTTP_201_CREATED
        )

class AddressListCreateView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyAddressesView(ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    # VIEW PARA EDITAR E DELETAR UM ADDRESS (GET,PATCH,PUT,DELETE)
class AddressDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        #VERIFICA SE O ENDEREÇO É DEFAULT
        if instance.is_default:
            total_addresses = Address.objects.filter(user=instance.user).count()
        
            if total_addresses == 1:
                raise ValidationError("Você não pode deletar o único endereço padrão")
        instance.delete()
    
# View para adicionar wishlist profile
class AddToWishlistView(CreateAPIView):
    serializer_class = AddWishlistSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = serializer.save()

        response_serializer = WishlistSerializer(item)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

# view para listar a wishlist
class WishlistListView(ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(
            profile=self.request.user.profile
        ).order_by("-created_at")
    
# View para adicionar wishlist profile
class RemoveWishlistView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(
            profile=self.request.user.profile
        )