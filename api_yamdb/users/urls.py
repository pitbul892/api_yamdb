from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import send_confirmation_code
from .views import create_token
from .views import UserViewSet


router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', send_confirmation_code),
    path('auth/token/', create_token),
]
