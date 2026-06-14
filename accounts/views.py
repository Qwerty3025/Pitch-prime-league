from django.shortcuts import render, get_object_or_404
from .models import Player

def player_list(request):
    players = Player.objects.select_related('current_team', 'stats').all()
    return render(request, 'players.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player.objects.select_related('current_team', 'stats'), pk=pk)
    return render(request, 'single-player.html', {'player': player})

