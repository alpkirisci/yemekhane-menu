from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Add the 'tshirt_color' field to the admin interface
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('tshirt_color',)}),
    )
    # Optionally, display 'tshirt_color' in the list display
    list_display = BaseUserAdmin.list_display + ('tshirt_color',)

# Register your custom User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
