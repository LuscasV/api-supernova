from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,
    CheckoutView,
)

urlpatterns = [
    path("", CartDetailView.as_view()),
    path("add/", AddToCartView.as_view()),
    path("item/<int:item_id>/", UpdateCartItemView.as_view()),
    path("item/<int:item_id>/remove/", RemoveCartItemView.as_view()),
    path("clear/", ClearCartView.as_view()),
    path("checkout/", CheckoutView.as_view()),
]