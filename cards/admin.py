from django.contrib import admin
from .models import SecretCard, CardActivation

@admin.register(SecretCard)
class SecretCardAdmin(admin.ModelAdmin):
    list_display = ('card_type', 'description')
    search_fields = ('card_type',)

@admin.register(CardActivation)
class CardActivationAdmin(admin.ModelAdmin):
    list_display = ('card', 'match', 'activating_team', 'activation_minute', 'is_exhausted')
    list_filter = ('is_exhausted', 'match__season')

