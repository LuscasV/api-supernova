from django.contrib import admin
from .models import (
    Gender,
    Category,
    Product,
    ProductColor,
    Size,
    Color,
    ProductImage,
    ProductSize,
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


# =========================
# PRODUCT SIZE INLINE
# =========================
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductColorInline(admin.TabularInline):
    model = ProductColor
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
        "is_featured",
        "is_active",
    )
    list_filter = ("gender", "category", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}

    inlines = [
        ProductImageInline,
        ProductSizeInline,
        ProductColorInline,
    ]


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
