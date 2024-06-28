from django.urls import path

from .views import send_confirmation_code
from .views import create_token
from .views import me
from .views import username_endpoint
from .views import UserListCreateView


urlpatterns = [
    path('auth/signup/', send_confirmation_code),
    path('auth/token/', create_token),
    path('users/me/', me),
    path('users/<str:username>/', username_endpoint),
    path('users/', UserListCreateView.as_view()),
]
