from django.contrib import admin

from cardapp.models import Card


# Register your models here.


class CardAdmin(admin.ModelAdmin):
    list_display = ('card_holder', 'card_number', 'money', 'view_is_expired', 'view_is_active', 'expired_date')
    search_fields = ('card_holder__username', 'card_number')
    list_filter = ('expired_date',)
    date_hierarchy = 'expired_date' 
    readonly_fields = ('expired_date',) 
    empty_value_display = "-empty-"

    fieldsets = (
        ('Card info', {
            'fields': ('card_holder', 'card_number')
        }),
        ('Card security', {
            'fields': ('card_pin_code', 'expired_date')
        }),
        ('Balance', {
            'fields': ('money',)
        })
    )

    @admin.display(boolean=True, ordering="expired_date", description="Is Expired?")
    def view_is_expired(self, obj):
        return obj.is_expired  # True/False chiqaradi

    @admin.display(boolean=True, description="Is Active?")
    def view_is_active(self, obj):
        return obj.is_active  # True/False chiqaradi

admin.site.register(Card, CardAdmin)
