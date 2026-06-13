from django.shortcuts import render, get_object_or_404
from .models import Season

# Create your views here.

def season_list(request):
    seasons = Season.objects.all()
    return render(request, 'league/season_list.html', {'seasons': seasons})

def standings_table(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    standings = season.get_standings()
    return render(request, 'league/standings.html', {'season': season, 'teams': standings})
