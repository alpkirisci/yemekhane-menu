from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('tshirt_color',)

    fieldsets = BaseUserAdmin.fieldsets + (
         (None, {'fields': ('tshirt_color',)}),
     )

admin.site.register(User, UserAdmin)