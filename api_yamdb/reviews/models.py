from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.CharField(
        max_length=256, blank=True, null=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.title}, {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MaxValueValidator(10, message='Оценка должна быть не выше 10'),
            MinValueValidator(1, message='Оценка должна быть не ниже 1')
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title')
        ]

    def __str__(self):
        return self.text

class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='comments',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text