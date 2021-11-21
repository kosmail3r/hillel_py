from django.contrib import admin
from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['user', 'original', 'shortcut', 'redirect_count']
    list_filter = ['user']
    search_fields = ['original']
