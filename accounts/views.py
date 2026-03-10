from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import Address
from .serializers import RegisterSerializer, AddressSerializer

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
        