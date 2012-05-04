from accounts.models import Account, Terms, Settings
from django.contrib import admin

class TermsAdmin(admin.ModelAdmin):
    fields = 'name', 'description', 'timeframe', 'type'

class SettingsInline(admin.StackedInline):
    model = Settings
    max_num = 1

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name']}),
        ('Contact Info',    {'fields': ['address', 'city', 'state', 'zip', 'phone', 'email']}),
        ('Terms',           {'fields': ['terms']}),
    ]

    inlines = [SettingsInline,]

admin.site.register(Account, AccountAdmin)
admin.site.register(Terms, TermsAdmin)
