from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        # title = Title.objects.get(id=title_id)
        # return title
    
    def get_queryset(self):
        queryset = self.get_title().reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())