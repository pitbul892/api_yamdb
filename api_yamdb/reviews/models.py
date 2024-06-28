from django.contrib.auth import get_user_model
from django.db import models

from .validate import validate_score, validate_year


User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenreBaseModel):
    """Model Category."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBaseModel):
    """Model Genre."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Model Title."""

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска', validators=(validate_year,)
    )
    description = models.CharField(
        max_length=256, blank=True, null=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class ReviewCommentBaseModel(models.Model):
    """BaseModel Review and Comment."""

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(ReviewCommentBaseModel):
    """Model Review."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            validate_score,
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]


class Comment(ReviewCommentBaseModel):
    """Model Comment."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
