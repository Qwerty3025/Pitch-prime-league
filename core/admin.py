from django.contrib import admin
from .models import SpecialPoster,GameRule,EntertainmentFeature,DisciplineRule,PartnerLogo

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


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'sort_order')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)