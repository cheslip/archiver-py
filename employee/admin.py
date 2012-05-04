from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User
from employee.models import Employee
from employee.forms import RequiredInlineFormSet


class ProfileInline(admin.StackedInline):
    model = Employee
    fk_name = 'user'
    max_num = 1
    formset = RequiredInlineFormSet


def employee_ID(object):
    return object.employee.employee_id

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]

    list_display = ['username', employee_ID, 'first_name', 'last_name', 'email', 'last_login', 'is_staff']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)