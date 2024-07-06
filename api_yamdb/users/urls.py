from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    create_token,
    SendConfirmationCodeView,
    UserViewSet
)

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', create_token),
    path('auth/signup/', SendConfirmationCodeView.as_view()),
]
