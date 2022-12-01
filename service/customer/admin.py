from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'mobile_operator', 'tag')


admin.site.register(Customer, CustomerAdmin)
