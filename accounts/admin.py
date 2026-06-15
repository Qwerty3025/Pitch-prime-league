from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Player, PlayerStats


class PlayerStatsInline(admin.StackedInline):
    model = PlayerStats
    extra = 0


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'position',
        'current_team',
        'skill_rating',
        'draft_status',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'position',
        'draft_status',
        'current_team',
    )

    inlines = [
        PlayerStatsInline,
    ]