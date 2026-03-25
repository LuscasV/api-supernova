from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Address, User, WishlistItem
from .serializers import RegisterSerializer, AddressSerializer, WishlistSerializer, AddWishlistSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Bloco try para se der erro no register não salvar o user
        try:
            with transaction.atomic():

                user = serializer.save()

                # GERAR TOKEN
                token = default_token_generator.make_token(user)

                #GERAR LINK
                verification_link = f"http://127.0.0.1:8000/api/accounts/verify/{user.id}/{token}/"

                # ENVIAR EMAIL
                send_mail(
                    subject="Confirme seu email",
                    message=f"Clique no link para ativar sua conta: {verification_link}",
                    from_email=settings.EMAIL_HOST_USER,
                     recipient_list=[user.email],
                )
        except Exception as e:
            raise ValidationError("Erro ao criar usuário. Tente novamente!")

        return Response(
            {"message": "Usuário criado com sucesso. Verique seu email!"},
            status=status.HTTP_201_CREATED
        )
    

class VerifyEmailView(APIView):
    def get(self, request, user_id, token):
        user = get_object_or_404(User, id=user_id)

        if user.is_verified:
            return Response({"message": "Email já verificado"}, status=200)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()

            return Response({"message": "Email verificado com sucesso!"})
        return Response({"error": "Token inválido"}, status=400)

User = get_user_model()

class ResendVerificationEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_verified:
            return Response(
                {"message": "Email já verificado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # LIMITE PARA EVITAR SPAM DE RESEND VERIFICATION
        if user.last_verification_email:
            diff = timezone.now() - user.last_verification_email

            if diff < timedelta(minutes=5):
                return Response(
                    {"error": "Aguarde antes de solicitar outro email."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
        
        token = default_token_generator.make_token(user)
        verification_link = f"http://127.0.0.1:8000/api/accounts/verify/{user.id}/{token}/"

        send_mail(
                    subject="Confirme seu email",
                    message=f"Clique no link para ativar sua conta: {verification_link}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
        
        # Atualiza data do envio
        user.last_verification_email = timezone.now()
        user.save(update_fields=["last_verification_email"])

        return Response(
            {"message": "Email de verificação reenviado"},
            status=status.HTTP_200_OK
        )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
    
    # Bloquear login se usuário não verificado
        if not self.user.is_verified:
            raise ValidationError("Verifique seu email antes de fazer login")
    
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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