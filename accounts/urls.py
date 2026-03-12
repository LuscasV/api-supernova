from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, AddressListCreateView, MyAddressesView, AddressDetailView, AddToWishlistView, WishlistListView, RemoveWishlistView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("address/", AddressListCreateView.as_view()),
    path("address/<int:pk>", AddressDetailView.as_view(), name="address-detail"),
    path("my-addresses/", MyAddressesView.as_view(), name="my-adresses"),

    path("wishlist/", WishlistListView.as_view()),
    path("wishlist/add/", AddToWishlistView.as_view()),
    path("wishlist/<int:pk>/remove/", RemoveWishlistView.as_view()),

    # JWT
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]