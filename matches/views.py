from django.shortcuts import render, get_object_or_404
from .models import Match

def fixture_list(request):
    fixtures = Match.objects.filter(status__in=[Match.Status.UPCOMING, Match.Status.LIVE, Match.Status.HALF_TIME])
    return render(request, 'fixtures.html', {'fixtures': fixtures})

def result_list(request):
    results = Match.objects.filter(status=Match.Status.COMPLETED)
    return render(request, 'results.html', {'results': results})

def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    events = match.events.select_related('acting_team', 'associated_player').all()
    activations = match.card_activations.select_related('activating_team', 'card').all()
    
    # Calculate stats for comparison
    stats_list = []
    if hasattr(match, 'stats'):
        stats = match.stats
        raw_stats = [
            ('Possession', stats.home_possession, stats.away_possession, True),
            ('Shots On Target', stats.home_shots_on_target, stats.away_shots_on_target, False),
            ('Shots', stats.home_shots, stats.away_shots, False),
            ('Touches', stats.home_touches, stats.away_touches, False),
            ('Passes', stats.home_passes, stats.away_passes, False),
            ('Tackles', stats.home_tackles, stats.away_tackles, False),
            ('Clearances', stats.home_clearances, stats.away_clearances, False),
            ('Goals', match.home_score, match.away_score, False),
        ]
        for name, home_val, away_val, is_pct in raw_stats:
            home_num = float(home_val or 0)
            away_num = float(away_val or 0)
            total = home_num + away_num
            if total > 0:
                home_pct = (home_num / total) * 100
                away_pct = (away_num / total) * 100
            else:
                home_pct = 50
                away_pct = 50
            
            stats_list.append({
                'name': name,
                'home_value': f"{int(home_num)}%" if is_pct else int(home_num),
                'away_value': f"{int(away_num)}%" if is_pct else int(away_num),
                'home_pct': home_pct,
                'away_pct': away_pct,
            })
            
    # Compile unified chronological event log
    timeline_events = []
    for e in events:
        detail_str = ""
        icon_class = ""
        if e.event_type == 'goal':
            detail_str = f"Goal scored by {e.associated_player}"
            if hasattr(e, 'goalevent'):
                ge = e.goalevent
                if ge.is_own_goal:
                    detail_str = f"Own Goal by {e.associated_player}"
                elif ge.is_assisted and ge.assistant_player:
                    detail_str = f"Goal scored by {e.associated_player} (Assisted by {ge.assistant_player})"
            icon_class = "fa fa-futbol-o text-success"
        elif e.event_type == 'card':
            card_color = "Yellow"
            icon_class = "fa fa-square text-warning"
            if hasattr(e, 'cardevent'):
                ce = e.cardevent
                card_color = ce.get_card_color_display()
                if ce.card_color == 'red':
                    icon_class = "fa fa-square text-danger"
            detail_str = f"{card_color} Card shown to {e.associated_player}"
        elif e.event_type == 'penalty':
            is_scored = False
            if hasattr(e, 'penaltyevent'):
                is_scored = e.penaltyevent.is_scored
            outcome = "scored" if is_scored else "missed"
            detail_str = f"Penalty {outcome} by {e.associated_player}"
            icon_class = "fa fa-dot-circle-o text-info"
        
        timeline_events.append({
            'minute': e.timestamp_minute,
            'type': e.event_type,
            'team': e.acting_team,
            'detail': detail_str,
            'icon': icon_class,
        })
        
    for a in activations:
        timeline_events.append({
            'minute': a.activation_minute,
            'type': 'activation',
            'team': a.activating_team,
            'detail': f"Secret Card Activated: {a.card}",
            'description': a.card.description,
            'icon': "fa fa-magic text-purple",
            'card_name': str(a.card),
        })
        
    timeline_events.sort(key=lambda x: x['minute'])
            
    return render(request, 'single-result.html', {
        'match': match,
        'events': events,
        'activations': activations,
        'stats_list': stats_list,
        'timeline_events': timeline_events,
    })






