from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (
    IsAuthenticatedUserAdminOrReadOnly,
    IsAuthenticatedAuthorModeratorAdminOrAuth,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class CategoryGenreBaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """CategoryGenreBaseViewSet"""

    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CategoryViewSet(CategoryGenreBaseViewSet):
    """ViewSet for Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedUserAdminOrReadOnly]


class GenreViewSet(CategoryGenreBaseViewSet):
    """ViewSet for Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedUserAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for Title."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAuthenticatedUserAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedAuthorModeratorAdminOrAuth,)

    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthorModeratorAdminOrAuth,)

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id, title=title_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
