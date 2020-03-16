from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
            (None, {
                'fields': ('birth_date',), }),
    )
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
            (None,
                {'fields': ('birth_date', 'random_number')}),
    )

    list_display = ['username', 'email', 'birth_date', 'random_number']


admin.site.register(CustomUser, CustomUserAdmin)
