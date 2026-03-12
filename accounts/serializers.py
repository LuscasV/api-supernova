from .models import Profile, WishlistItem, Address
from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Product, Size, Color

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    cpf = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "cpf",
            "email",
            "password",
            "password2",
        ]

    def validate(self, data):
        if data["password"] !=data["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem"})
        return data
    
    def validate_cpf(self, value):
        if Profile.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF já cadastrado.")
        return value
        
    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        cpf = validated_data.pop("cpf")
        validated_data.pop("password2")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        Profile.objects.create(
            user=user,
            full_name=full_name,
            cpf=cpf
        )

        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "number",
            "neighborhood",
            "city",
            "state",
            "zip_code",
            "is_default",
        ]
    def create(self, validated_data):
        user = validated_data["user"]

        if validated_data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = instance.user

        if validated_data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).exclude(id=instance.id).update(is_default=False)

        return super().update(instance, validated_data)

# serializer da wishlist
class WishlistSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    size = serializers.CharField(source="size.name", read_only=True)
    color = serializers.CharField(source="color.name", read_only=True)
    color_hex = serializers.CharField(source="color.hex_code", read_only=True)

    product_image = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product_id",
            "product_name",
            "product_price",
            "size",
            "color",
            "color_hex",
            "product_image",
            "created_at",
        ]
    def get_product_image(self, obj):
        image = obj.product.images.filter(is_main=True).first()
        if image:
            return image.image.url
        return None

class AddWishlistSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    size_id = serializers.IntegerField(required=False)
    color_id = serializers.IntegerField(required=False)

    def create(self, validated_data):

        request = self.context["request"]
        profile = request.user.profile
        product_id = validated_data["product_id"]

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produto não encontrado.")

        wishlist_item, created = WishlistItem.objects.get_or_create(
            profile=profile,
            product=product,
        )

        if not created:
            raise serializers.ValidationError(
                {"message": "Produto já está na wishlist."}
            )

        return wishlist_item