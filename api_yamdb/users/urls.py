from django.urls import path

from .views import send_confirmation_code
from .views import create_token
from .views import me
from .views import username_endpoint
from .views import UserListCreateView


urlpatterns = [
    path('signup/', send_confirmation_code),
    path('token/', create_token),
    path('me/', me),
    path('<str:username>/', username_endpoint),
    path('', UserListCreateView.as_view()),
]
