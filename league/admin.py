from django.contrib import admin
from .models import League, Season, Team
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


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'league', 'season_number', 'is_active', 'start_date', 'end_date')
    list_filter = ('league', 'is_active')
    list_editable = ('is_active',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'season',
        'president',
        'manager_name',
        'games_played',
        'wins',
        'draws',
        'losses',
        'total_points',
        'goals_for',
        'goals_against',
    )
    list_filter = ('season',)
    search_fields = ('name', 'manager_name', 'location')
    inlines = [
        PlayerInline,
    ]


    