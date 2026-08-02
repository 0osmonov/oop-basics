from rest_framework import serializers

from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    name = serializers.CharField(min_length=1, max_length=255)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        if hasattr(obj, 'products_count'):
            return obj.products_count
        return obj.products.count()

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Название не может быть пустым')

        queryset = Category.objects.filter(name__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Категория с таким названием уже существует')

        return value


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1, max_length=255)
    description = serializers.CharField(min_length=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Название не может быть пустым')
        return value

    def validate_description(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Описание не может быть пустым')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(min_length=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Текст отзыва не может быть пустым')
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']
