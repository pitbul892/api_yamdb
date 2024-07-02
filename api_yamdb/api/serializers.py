from datetime import date

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.constants import NAME_MAX_LENGTH
from reviews.validate import validate_score
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer Read Title."""

    name = serializers.CharField(max_length=NAME_MAX_LENGTH)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Serializer Write Title."""

    name = serializers.CharField(max_length=256)
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        this_year = date.today().year
        if value > this_year:
            raise serializers.ValidationError('Ошибка в указанном году')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review."""

    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(validators=[validate_score])

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
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
