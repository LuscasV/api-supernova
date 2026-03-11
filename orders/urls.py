from django.urls import path
from .views import OrderCreateView, MyOrdersListView, OrderDetailView, CancelOrderView

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("my-orders/", MyOrdersListView.as_view(), name="my-orders"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/cancel/", CancelOrderView.as_view(), name="order-cancel"),
]