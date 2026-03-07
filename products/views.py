from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Gender
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        gender = self.request.query_params.get("gender")
        category = self.request.query_params.get("category")

        if gender:
            queryset = queryset.filter(gender__slug=gender)

        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset


class FeaturedProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(
        is_active=True,
        is_featured=True
    )
    serializer_class = ProductSerializer


class ProductByGenderView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        gender_slug = self.kwargs["gender_slug"]

        return Product.objects.filter(
            gender__slug=gender_slug,
            is_active=True
        )

class ProductByGenderCategoryView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        gender_slug = self.kwargs["gender_slug"]
        category_slug = self.kwargs["category_slug"]

        return Product.objects.filter(
            gender__slug=gender_slug,
            category__slug=category_slug,
            is_active=True
        )


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

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            gender__slug=self.kwargs["gender_slug"],
            category__slug=self.kwargs["category_slug"],
        )

    lookup_field = "slug"
    lookup_url_kwarg = "product_slug"