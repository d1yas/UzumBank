from django.contrib import admin

from cardapp.models import Card, UserProfile, Course


# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ('card_holder', 'money', 'is_expired','is_active')
    search_fields = ('card_holder',)
    #adminkani to`liq o`rganish


admin.site.register(Card, CardAdmin)
admin.site.register(UserProfile)
admin.site.register(Course)
