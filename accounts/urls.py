from django.urls import path
from .views import RegisterView, AddressListCreateView, MyAddressesView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("address/", AddressListCreateView.as_view()),
    path("my-addresses/", MyAddressesView.as_view(), name="my-adresses"),
]