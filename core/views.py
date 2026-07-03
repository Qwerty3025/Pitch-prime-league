from django.shortcuts import render

from .models import SpecialPoster, GameRule, EntertainmentFeature, DisciplineRule
from league.models import Season
from matches.models import Match


def base(request):
    return render(request, 'base.html')


def home(request):
    current_season = Season.objects.filter(is_active=True).order_by('-season_number').first()
    standings = current_season.get_standings() if current_season else []

    recent_results = Match.objects.filter(status=Match.Status.COMPLETED).order_by('-scheduled_time')[:5]
    next_match = Match.objects.filter(status__in=[Match.Status.UPCOMING, Match.Status.LIVE, Match.Status.HALF_TIME]).order_by('scheduled_time').first()
    featured_poster = SpecialPoster.objects.filter(is_active=True).order_by('-created_at').first()

    context = {
        'current_season': current_season,
        'standings': standings,
        'recent_results': recent_results,
        'next_match': next_match,
        'featured_poster': featured_poster,
    }
    return render(request, 'home.html', context)



from django.shortcuts import render

from .models import (
    GameRule,
    EntertainmentFeature,
    DisciplineRule
)





def rules(request):

    context = {

        "rules": GameRule.objects.all(),

        "features": EntertainmentFeature.objects.all(),

        "discipline": DisciplineRule.objects.all(),

    }


    return render(
        request,
        "rules.html",
        context
    )

def contact(request):
    return render(request, 'contact.html')