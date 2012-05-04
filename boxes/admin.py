from boxes.models import Box, BoxItem
from django.db import models
from django.contrib import admin
from django.forms import TextInput
from reversion.helpers import patch_admin

class BoxItemInline(admin.TabularInline):
    model=BoxItem
    fields = ['slot', 'accession', 'donor_id', 'tube_type', 'user', 'date', 'used']
    extra = 0

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 15})},
    }

class BoxAdmin(admin.ModelAdmin):
    fields = 'account', 'number'
    list_filter = ['account']
    inlines = [BoxItemInline]

class BoxItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Box Info',        {'fields': ['box', 'slot']}),
        ('Sample Info',     {'fields': ['accession', 'donor_id', 'tube_type']}),
        ('Archive Info',    {'fields': ['user', 'date']}),
    ]

    list_display = ['slot', 'box', 'accession', 'donor_id', 'tube_type', 'user', 'date']
    list_filter = ['box__account']
    search_fields = ['box__number']

admin.site.register(Box, BoxAdmin)
admin.site.register(BoxItem, BoxItemAdmin)
patch_admin(BoxItem)
patch_admin(Box)