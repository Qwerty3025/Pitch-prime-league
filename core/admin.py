from django.contrib import admin
from .models import SpecialPoster

@admin.register(SpecialPoster)
class SpecialPosterAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)

