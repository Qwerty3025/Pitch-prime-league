from django.contrib import admin


# Register your models here.
# match/admin.py
from django.contrib import admin
from .models import Match



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
    )

    list_filter = (
        'status',
        'season',
    )

