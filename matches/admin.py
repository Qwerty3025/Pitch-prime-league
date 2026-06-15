# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Match, MatchEvent, GoalEvent, CardEvent, PenaltyEvent

class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 1

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'season', 'scheduled_time', 'status', 'home_score', 'away_score')
    list_filter = ('season', 'status')
    inlines = [MatchEventInline]
    date_hierarchy = 'scheduled_time'

@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'timestamp_minute', 'event_type', 'acting_team', 'associated_player')
    list_filter = ('event_type', 'match__season')

@admin.register(GoalEvent)
class GoalEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'timestamp_minute', 'acting_team', 'associated_player', 'is_own_goal', 'is_assisted')

@admin.register(CardEvent)
class CardEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'timestamp_minute', 'acting_team', 'associated_player', 'card_color')

@admin.register(PenaltyEvent)
class PenaltyEventAdmin(admin.ModelAdmin):
    list_display = ('match', 'timestamp_minute', 'acting_team', 'associated_player', 'is_scored', 'penalty_type')

