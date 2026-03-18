from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from .models import Product, Category, Gender
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import Q


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull=True)
        gender = self.request.query_params.get("gender")

        if gender:
            queryset = queryset.filter(products__gender__slug=gender).distinct()

        return queryset


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by("-created_at")

        gender = self.request.query_params.get("gender")
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")

        if gender:
            queryset = queryset.filter(gender__slug=gender)

        if category:
            queryset = queryset.filter(category__slug=category)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        return queryset


class MenuView(APIView):
    def get(self, request):
        data = []

        genders = Gender.objects.all()

        for gender in genders:
            categories = Category.objects.filter(parent__isnull=True)

            data.append({
                "gender": {
                    "name": gender.name,
                    "slug": gender.slug,
                },
                "categories": [
                    {
                        "name": category.name,
                        "slug": category.slug,
                        "children": [
                            {
                                "name": child.name,
                                "slug": child.slug,
                            }
                            for child in category.subcategories.all()
                        ],
                    }
                    for category in categories
                ],
            })

        return Response(data)

class ProductDetailBySlugView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)

    lookup_field = "slug"
    lookup_url_kwarg = "product_slug"

    # def get_queryset(self):
    #     return Product.objects.filter(
    #         is_active=True,
    #         gender__slug=self.kwargs["gender_slug"],
    #         category__slug=self.kwargs["category_slug"],
    #     )

    # lookup_field = "slug"
    # lookup_url_kwarg = "product_slug"

class FeaturedProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            is_featured=True
        )