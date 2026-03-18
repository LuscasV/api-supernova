from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product, ProductVariant

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]  

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE
    )

    order_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    # ENDEREÇO CONGELADO NO MOMENTO DA COMPRA
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    status_updated_at = models.DateTimeField(auto_now=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
    
        if creating and not self.order_number:
            date = timezone.now().strftime("%Y%m%d")
            self.order_number = f"ORD-{date}-{self.id:04d}"
            super().save(update_fields=["order_number"])

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )

    def get_total(self): 
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.size} - {self.color}"