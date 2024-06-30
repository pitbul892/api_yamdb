from django.urls import path

from .views import (
    UserListCreateView,
    create_token,
    me,
    send_confirmation_code,
    username_endpoint,
)

urlpatterns = [
    path('auth/signup/', send_confirmation_code),
    path('auth/token/', create_token),
    path('users/me/', me),
    path('users/<str:username>/', username_endpoint),
    path('users/', UserListCreateView.as_view()),
]
