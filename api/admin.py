from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Store)


class StoreAdmin(admin.ModelAdmin):
    list_display = '__all__'
