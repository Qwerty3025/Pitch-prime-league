from django.shortcuts import render, get_object_or_404
from .models import Match

def fixture_list(request):
    fixtures = Match.objects.filter(status__in=[Match.Status.UPCOMING, Match.Status.LIVE])
    return render(request, 'fixtures.html', {'fixtures': fixtures})

def result_list(request):
    results = Match.objects.filter(status=Match.Status.COMPLETED)
    return render(request, 'results.html', {'results': results})

def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    events = match.events.select_related('acting_team', 'associated_player').all()
    activations = match.card_activations.select_related('activating_team', 'card').all()
    return render(request, 'single-result.html', {
        'match': match,
        'events': events,
        'activations': activations,
    })

