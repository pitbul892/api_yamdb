from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, ReviewViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
<<<<<<<<< Temporary merge branch 1

urlpatterns = [
    path("v1/", include(router.urls)),
]
=========
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
