from django.contrib import admin
from .models import Search
# Register your models here.

class SearchAdmin(admin.ModelAdmin):
    list_display = ('title','address', 'url', 'image', 'review_count', 'rating')

admin.site.register(Search, SearchAdmin)