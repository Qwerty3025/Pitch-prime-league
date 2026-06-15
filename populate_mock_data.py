import os
import django
import shutil
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primeleague.settings')
django.setup()

from django.utils import timezone
from league.models import League, Season, Team
from matches.models import Match
from core.models import SpecialPoster
from accounts.models import President, Player, PlayerStats
from cards.models import SecretCard

def populate():
    print("Populating Pitch Prime League mock data...")

    # 1. Ensure Media folder exists for posters
    media_posters_dir = os.path.join('media', 'posters')
    os.makedirs(media_posters_dir, exist_ok=True)
    
    # Copy a sample image from static assets to represent the poster image
    sample_src = os.path.join('static', 'img', 'blog', '1.jpg')
    sample_dest = os.path.join(media_posters_dir, 'kickoff.jpg')
    if os.path.exists(sample_src):
        shutil.copy(sample_src, sample_dest)
        print("Copied sample poster image to media/posters/kickoff.jpg")

    # 2. Create League
    league, _ = League.objects.get_or_create(name="Pitch Prime League")

    # 3. Create Season
    # Deactivate other seasons first
    Season.objects.all().update(is_active=False)
    season, created = Season.objects.get_or_create(
        league=league,
        season_number=1,
        defaults={
            'start_date': datetime.now().date() - timedelta(days=30),
            'end_date': datetime.now().date() + timedelta(days=60),
            'is_active': True
        }
    )
    if not created:
        season.is_active = True
        season.save()

    # 4. Create 8 Teams and Presidents
    team_data = [
        ("Lagos Ninjas", "https://twitter.com/lagos_ninjas"),
        ("Abuja Eagles", "https://twitter.com/abuja_eagles"),
        ("Kano Kings", "https://twitter.com/kano_kings"),
        ("Port Harcourt Pirates", "https://twitter.com/ph_pirates"),
        ("Ibadan Warriors", "https://twitter.com/ibadan_warriors"),
        ("Enugu Rangers", "https://twitter.com/enugu_rangers"),
        ("Calabar Rovers", "https://twitter.com/calabar_rovers"),
        ("Benin Vipers", "https://twitter.com/benin_vipers")
    ]

    teams = []
    for idx, (name, social) in enumerate(team_data, start=1):
        # Create a President (subclass of User)
        email = f"pres_{idx}@ppl.com"
        president, _ = President.objects.get_or_create(
            email=email,
            defaults={
                'name': f"President {name}",
                'role': 'president',
                'social_media_channel': social
            }
        )
        
        # Create Team
        team, _ = Team.objects.get_or_create(
            season=season,
            name=name,
            defaults={
                'president': president,
                'logo': None
            }
        )
        teams.append(team)

    print(f"Created/Verified {len(teams)} teams.")

    # 5. Create Completed Matches to populate standings table
    # Reset team stats first
    for t in teams:
        t.games_played = 0
        t.wins = 0
        t.draws = 0
        t.losses = 0
        t.total_points = 0
        t.goals_for = 0
        t.goals_against = 0
        t.save()

    # Match results template: (HomeTeamIndex, AwayTeamIndex, HomeScore, AwayScore, DaysAgo)
    results = [
        (0, 1, 3, 1, 10),  # Lagos 3 - 1 Abuja
        (2, 3, 2, 2, 9),   # Kano 2 - 2 PH
        (4, 5, 1, 0, 8),   # Ibadan 1 - 0 Enugu
        (6, 7, 0, 2, 7),   # Calabar 0 - 2 Benin
        (1, 2, 1, 0, 6),   # Abuja 1 - 0 Kano
        (3, 4, 3, 2, 5),   # PH 3 - 2 Ibadan
        (5, 6, 2, 1, 4),   # Enugu 2 - 1 Calabar
        (7, 0, 0, 4, 3),   # Benin 0 - 4 Lagos
    ]

    for h_idx, a_idx, h_score, a_score, days_ago in results:
        h_team = teams[h_idx]
        a_team = teams[a_idx]
        
        # Create completed Match
        match = Match.objects.create(
            season=season,
            home_team=h_team,
            away_team=a_team,
            scheduled_time=timezone.now() - timedelta(days=days_ago),
            status='completed',
            home_score=h_score,
            away_score=a_score
        )
        # Recalculate stands is automatically triggered on Match save()

    print("Created 8 completed matches. Standings computed.")

    # 6. Create Upcoming Match (For countdown)
    Match.objects.filter(status='upcoming').delete()
    upcoming_time = timezone.now() + timedelta(days=4, hours=6, minutes=30)
    upcoming_match = Match.objects.create(
        season=season,
        home_team=teams[0],  # Lagos Ninjas
        away_team=teams[1],  # Abuja Eagles
        scheduled_time=upcoming_time,
        status='upcoming'
    )
    print(f"Created upcoming match: {upcoming_match} scheduled at {upcoming_time}")

    # 7. Create Special Poster
    SpecialPoster.objects.all().delete()
    poster = SpecialPoster.objects.create(
        title="Pitch Prime League Grand Kickoff 2026: Tickets Live Next Week!",
        image="posters/kickoff.jpg",
        target_url="https://pitchprimeleague.com/events/kickoff-2026",
        is_active=True
    )
    print(f"Created Special Poster: '{poster.title}'")

    print("\nData population successful! Run 'python manage.py runserver' to view the site.")

if __name__ == '__main__':
    populate()
