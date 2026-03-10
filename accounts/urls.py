from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, AddressListCreateView, MyAddressesView, AddressDetailView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("address/", AddressListCreateView.as_view()),
    path("address/<int:pk>", AddressDetailView.as_view(), name="address-detail"),
    path("my-addresses/", MyAddressesView.as_view(), name="my-adresses"),

    # JWT
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]