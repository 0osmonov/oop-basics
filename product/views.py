from django.db.models import Avg, Count
from rest_framework import generics

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductReviewsListAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').annotate(
        rating=Avg('reviews__stars'),
    )
    serializer_class = ProductWithReviewsSerializer


class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
