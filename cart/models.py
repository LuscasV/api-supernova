from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.get_total() for item in self.items.all())
    
    def __str__(self):
        return f"Carrinho de {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.get_current_price() * self.quantity
    
    class Meta:
        unique_together = ("cart", "variant")

    def __str__(self):
        return f"self{self.product.name} - {self.quantity}"