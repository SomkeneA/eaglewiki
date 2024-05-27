from django.contrib import admin
from .models import Entry 
from django.utils.html import format_html

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag')

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />'.format(obj.thumbnail.url)) # type: ignore
        return ""
    thumbnail_tag.short_description = 'Thumbnail'

admin.site.register(Entry, EntryAdmin)