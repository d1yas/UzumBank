from django.contrib import admin

from cardapp.models import Card


# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ('card_holder', 'money', 'is_expired','is_active')
    search_fields = ('card_holder',)


admin.site.register(Card, CardAdmin)
