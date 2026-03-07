from django.urls import path
from .views import (
    ProductByGenderView,
    ProductByGenderCategoryView,
    ProductDetailBySlugView,
)

urlpatterns = [
    path(
        "products/<slug:gender_slug>/",
        ProductByGenderView.as_view(),
        name="products-by-gender"
    ),
    path(
        "products/<slug:gender_slug>/<slug:category_slug>/",
        ProductByGenderCategoryView.as_view(),
        name="products-by-gender-category"
    ),
    # Detalhe do produto por slug
    path(
        "products/<slug:gender_slug>/<slug:category_slug>/<slug:product_slug>/",
        ProductDetailBySlugView.as_view(),
        name="product-detail-by-slug"
    ),
]
