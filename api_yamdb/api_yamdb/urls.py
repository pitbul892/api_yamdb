"""YaMDb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import send_confirmation_code, create_token
from users.views import me
from users.views import UsersViewSet, UsersMeViewSet

router = DefaultRouter()
# router.register('api/v1/users/me', UsersMeViewSet)
router.register('api/v1/users', UsersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', send_confirmation_code),
    path('api/v1/auth/token/', create_token),
    path('api/v1/users/me/', me),
    path('', include(router.urls)),
]
