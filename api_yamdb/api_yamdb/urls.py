from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/users/', include('users.urls')),
]
