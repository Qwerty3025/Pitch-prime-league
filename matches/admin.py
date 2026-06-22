from django.contrib import admin


# Register your models here.
# match/admin.py
from django.contrib import admin
from .models import Match, MatchStats



# @admin.register(Match)
# class MatchAdmin(admin.ModelAdmin):
#     list_display = (
#         'home_team',
#         'away_team',
#         'season',
#         'scheduled_time',
#         'status',
#         'home_score',
#         'away_score',
#     )

#     list_filter = (
#         'status',
#         'season',
#     )

class MatchStatsInline(admin.StackedInline):
    model = MatchStats
    extra = 0

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = (
        'home_team',
        'away_team',
        'season',
        'scheduled_time',
        'status',
        'home_score',
        'away_score',
        'winner',
    )

    inlines = [
        MatchStatsInline,
    ]

    list_filter = (
        'status',
        'season',
    )

    search_fields = (
        'home_team__name',
        'away_team__name',
    )

    list_editable = (
        'status',
        'home_score',
        'away_score',
    )

    def winner(self, obj):
        winner = obj.get_winner()
        return winner.name if winner else "Draw"

    winner.short_description = "Winner"


@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):

    list_display = (
        'match',
        'home_possession',
        'away_possession',
        'home_shots',
        'away_shots',
    )

