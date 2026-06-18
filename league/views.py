from django.shortcuts import render, get_object_or_404
from .models import Season, Team
from matches.models import Match
from accounts.models import Player

# Create your views here.

def season_list(request):
    seasons = Season.objects.all()
    return render(request, 'league/season_list.html', {'seasons': seasons})

def standings_table(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    standings = season.get_standings()

    # Aggregate season stats for the info bar
    total_matches_played = season.matches.filter(status='completed').count()
    total_goals = sum(
        (m.home_score or 0) + (m.away_score or 0)
        for m in season.matches.filter(status='completed')
    )
    avg_goals = round(total_goals / total_matches_played, 1) if total_matches_played else 0

    context = {
        'season': season,
        'standings': standings,
        'total_matches_played': total_matches_played,
        'total_goals': total_goals,
        'avg_goals': avg_goals,
    }
    return render(request, 'league/standings.html', context)

def team(request):
    teams = Team.objects.select_related(
        'season',
        'president'
    ).order_by('name')

    context = {
        'teams': teams,
    }
    return render(request, 'teams.html', context)

from django.db.models import Q

from django.db.models import Q
from matches.models import Match

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

    fixtures = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status__in=[Match.Status.UPCOMING, Match.Status.LIVE]
    ).order_by('scheduled_time')

    results = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        status=Match.Status.COMPLETED
    ).order_by('-scheduled_time')

    context = {
        'team': team,
        'players': players,
        'fixtures': fixtures,
        'results': results,
    }

    return render(request, 'team_detail.html', context)

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)

    return render(request, 'single-player.html', {
        'player': player
    })
