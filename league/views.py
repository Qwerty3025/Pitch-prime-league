from django.shortcuts import render, get_object_or_404
from .models import Season, Team

# Create your views here.

def season_list(request):
    seasons = Season.objects.all()
    return render(request, 'league/season_list.html', {'seasons': seasons})

def standings_table(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    standings = season.get_standings()
    return render(request, 'league/standings.html', {'season': season, 'teams': standings})

def team(request):
    teams = Team.objects.select_related(
        'season',
        'president'
    ).order_by('name')

    context = {
        'teams': teams,
    }
    return render(request, 'teams.html', context)

def team_detail(request, pk):
    team = get_object_or_404(
        Team.objects.select_related(
            'season',
            'president'
        ).prefetch_related(
            'players__stats'
        ),
        pk=pk
    )

    players = team.players.all()

    context = {
        'team': team,
        'players': players,
    }

    return render(request, 'team_detail.html', context)
