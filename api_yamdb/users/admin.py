from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustUser

admin.site.register(CustUser, UserAdmin)
