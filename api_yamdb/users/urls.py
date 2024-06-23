from django.urls import include, path
from rest_framework import routers

from users.views import (create_token, me,
                         send_confirmation_code, UsersViewSet)

router = routers.DefaultRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', create_token),
    path('v1/users/me/', me),
    path('v1/', include(router.urls)),
]
