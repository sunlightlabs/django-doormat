from django.contrib import admin
from doormat.models import DoorMat

class DoorMatAdmin(admin.ModelAdmin):
    list_display = ('domain', 'path', 'is_enabled', 'last_published')
    list_display_links = ('domain', 'path')
    list_filter = ('is_enabled', 'domain')
    readonly_fields = ('last_published',)
    search_fields = ('domain', 'path', 'content')
admin.site.register(DoorMat, DoorMatAdmin)