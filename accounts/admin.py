from django.contrib import admin
from .models import User, President, Player, PlayerStats
from django.utils.html import format_html

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
    def profile_thumbnail(self, obj):
        if getattr(obj, 'profile_image', None):
            return format_html('<img src="{}" style="width:45px;height:auto;border-radius:50%;" />', obj.profile_image.url)
        return ''

    profile_thumbnail.short_description = 'Photo'

    def description_summary(self, obj):
        if obj.description:
            return obj.description[:75] + ('...' if len(obj.description) > 75 else '')
        return '-'

    description_summary.short_description = 'Description'

    list_display = ('profile_thumbnail', 'name', 'description_summary', 'email', 'position', 'draft_status', 'skill_rating', 'current_team')
    list_filter = ('position', 'draft_status', 'current_team')
    search_fields = ('name', 'email', 'description')
    fields = ('name', 'email', 'role', 'position', 'draft_status', 'skill_rating', 'description', 'profile_image', 'current_team')
    inlines = [PlayerStatsInline]

@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'goals', 'assists', 'mvp_awards', 'yellow_cards', 'red_cards')
    search_fields = ('player__name',)

