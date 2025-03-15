from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_year', 'birth_month', 'birth_days',)
    search_fields = ('first_name', 'last_name')
    list_filter = ('birth_year', 'birth_month')
    empty_value_display = "-empty-"

    fieldsets = (
        ('User Info', {
            'fields': ('first_name', 'last_name', 'birth_year', 'birth_month', 'birth_days')
        }),
        ('Security', {
            'fields': ('password',)
        })
    )

admin.site.register(User, UserAdmin)
