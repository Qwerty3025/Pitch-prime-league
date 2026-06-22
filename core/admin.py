from django.contrib import admin
from .models import SpecialPoster,GameRule,EntertainmentFeature,DisciplineRule

@admin.register(SpecialPoster)
class SpecialPosterAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)






@admin.register(GameRule)
class GameRuleAdmin(admin.ModelAdmin):

    list_display = (
        'number',
        'title',
    )

    ordering = (
        'number',
    )




@admin.register(EntertainmentFeature)
class EntertainmentFeatureAdmin(admin.ModelAdmin):

    list_display = (
        'title',
    )




@admin.register(DisciplineRule)
class DisciplineRuleAdmin(admin.ModelAdmin):

    list_display = (
        'rule',
    )