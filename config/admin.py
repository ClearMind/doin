from django.contrib.admin import  site, ModelAdmin
from config.models import MenuItem, NewsItem

class MenuItemAdmin(ModelAdmin):
    list_display = ('name', 'link', 'public')
    ordering = ['order']

site.register(MenuItem, MenuItemAdmin)
site.register(NewsItem)