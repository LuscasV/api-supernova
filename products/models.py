from django.db import models

class Gender(models.Model):
    name = models.CharField(max_length=20)  # Masculino, Feminino, Unissex
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("slug", "parent")

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=30)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True)

    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_sizes"
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE
    )
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"

    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagem de {self.product.name}"
    
class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="colors",
        on_delete=models.CASCADE
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "color")

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"