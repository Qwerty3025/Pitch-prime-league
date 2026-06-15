from django.shortcuts import render
from league.models import Team, Season
from matches.models import Match
from .models import SpecialPoster # Assuming SpecialPoster is in core/models.py


def base(request):
    return render(request, 'base.html')

def home(request):
    # Fetch current active season
    current_season = Season.objects.filter(is_active=True).first()
    
    # Fetch standings using model logic (sorting by points, goal difference, goals for)
    standings = current_season.get_standings()[:8] if current_season else []
    
    # Get the single most recent active poster
    featured_poster = SpecialPoster.objects.filter(is_active=True).order_by('-created_at').first()
    
    # Get the next upcoming match for the countdown (fix match_date -> scheduled_time)
    next_match = Match.objects.filter(status='upcoming').order_by('scheduled_time').first()
    
    # Fetch recent completed matches for the homepage results tab
    recent_results = Match.objects.filter(status='completed').order_by('-scheduled_time')[:3]
    
    # Fetch upcoming matches for the fixtures tab
    upcoming_matches = Match.objects.filter(status='upcoming').order_by('scheduled_time')[:3]
    
    return render(request, 'home.html', {
        'current_season': current_season,
        'standings': standings,
        'featured_poster': featured_poster,
        'next_match': next_match,
        'recent_results': recent_results,
        'upcoming_matches': upcoming_matches,
    })

