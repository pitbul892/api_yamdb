from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SendConfirmationCodeViewSet
from .views import create_token
from .views import UserViewSet


router = SimpleRouter()
router.register('users', UserViewSet)
router.register('auth/signup', SendConfirmationCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', create_token),
]
