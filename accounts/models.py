from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from products.models import Product, Size, Color

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    last_verification_email = models.DateTimeField(null=True, blank=True)
    last_password_reset_request = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.full_name


class Address(models.Model):
    user = models.ForeignKey(
        User, 
        related_name="addresses",
        on_delete=models.CASCADE
    )
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.number}"

class WishlistItem(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name="wishlist_items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        related_name="wishlisted_by",
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "product") # impede de favoritar o mesmo produto 2 vezes
    
    def __str__(self):
        return f"{self.profile.full_name} - {self.product.name}"