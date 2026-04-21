from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    Gender,
    Category,
    Product,
    Size,
    Color,
    ProductImage,
    ProductVariant
)

# =========================
# GENDER
# =========================
@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


# =========================
# CATEGORY
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    prepopulated_fields = {"slug": ("name",)}


# =========================
# PRODUCT IMAGE INLINE
# =========================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

# =========================
# PRODUCT
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "gender",
        "category",
        "price",
        "promo_price",
        "is_on_sale",
        "promo_start",
        "promo_end",
        "is_featured",
        "is_active",
    )
    list_filter = ("gender", "category", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductImageInline,
        ProductVariantInline
    ]

    def is_on_sale(self, obj):
        return obj.get_current_price() != obj.price
    
    is_on_sale.boolean = True
    is_on_sale.short_description = "Em promoção"

    def save_model(self, request, obj, form, change):
        if obj.promo_price and obj.promo_price >= obj.price:
            raise ValidationError("O preço promocional deve ser menor que o preço normal.")

        if obj.promo_start and obj.promo_end:
            if obj.promo_start > obj.promo_end:
                raise ValidationError("A data de início não pode ser maior que a data final.")
            
        super().save_model(request, obj, form, change)

# =========================
# SIZE
# =========================
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name",)


# =========================
# COLOR
# =========================
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")
