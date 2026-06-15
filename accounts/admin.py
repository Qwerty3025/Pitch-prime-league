from django.contrib import admin
from .models import User, President, Player, PlayerStats

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('name', 'email')

@admin.register(President)
class PresidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'social_media_channel')
    search_fields = ('name', 'email')

class PlayerStatsInline(admin.StackedInline):
    model = PlayerStats
    extra = 0

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'draft_status', 'skill_rating', 'current_team')
    list_filter = ('position', 'draft_status', 'current_team')
    search_fields = ('name', 'email')
    inlines = [PlayerStatsInline]

@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'goals', 'assists', 'mvp_awards', 'yellow_cards', 'red_cards')
    search_fields = ('player__name',)

