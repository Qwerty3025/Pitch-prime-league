from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Team
from accounts.models import Player


class PlayerInline(admin.TabularInline):
    model = Player
    fk_name = 'current_team'
    extra = 0

    fields = (
        'name',
        'position',
        'skill_rating',
        'draft_status',
    )

    show_change_link = True


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'season',
        'president',
        'manager_name',
        'total_points',
    )

    search_fields = (
        'name',
        'manager_name',
        'location',
    )

    list_filter = (
        'season',
    )

    inlines = [
        PlayerInline,
    ]


    