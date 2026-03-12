from django.urls import path
from .views import (
    CategoryListView,
    ProductDetailBySlugView,
    FeaturedProductListView,
    ProductListView
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(),
         name="category-list"
         ),
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list"
    ),
    # Produto Destaque
    path(
        "products/featured/",
        FeaturedProductListView.as_view(),
        name="featured-products"
    ),
    path(
        "products/<slug:product_slug>/", ProductDetailBySlugView.as_view(),
        name="product-detail"
    ),
    # path(
    #     "products/<slug:gender_slug>/",
    #     ProductByGenderView.as_view(),
    #     name="products-by-gender"
    # ),
    # path(
    #     "products/<slug:gender_slug>/<slug:category_slug>/",
    #     ProductByGenderCategoryView.as_view(),
    #     name="products-by-gender-category"
    # ),
    # # Detalhe do produto por slug
    # path(
    #     "products/<slug:gender_slug>/<slug:category_slug>/<slug:product_slug>/",
    #     ProductDetailBySlugView.as_view(),
    #     name="product-detail-by-slug"
    # ),
]
