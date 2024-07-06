from django.contrib import admin
from .models import Draft

@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')
    search_fields = ('title',)
    list_filter = ('timestamp',)

