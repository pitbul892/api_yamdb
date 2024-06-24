from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Такой slug уже есть',
            )
        ],
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Такой slug уже есть',
            )
        ],
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField()
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Проверьте оценку!')
        return value

    def validate(self, data):
        author = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(author=author, title=title).exists()
        ):
            raise serializers.ValidationError('Отзыв уже существует')
        return data

    class Meta:
        fields = '__all__'
        model = Review
