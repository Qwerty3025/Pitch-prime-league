from django.db import models


class League(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, help_text="Mark this as the current live season")
    standings_table = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-season_number']
        unique_together = ['league', 'season_number']

    def get_standings(self):
        """Returns teams sorted by points, goal difference, and goals for."""
        teams = list(self.teams.all())
        teams.sort(key=lambda t: (t.total_points, t.goal_difference, t.goals_for), reverse=True)
        return teams

    def __str__(self):
        return f'{self.league.name} Season {self.season_number}'


class Team(models.Model):
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='teams'
    )

    president = models.OneToOneField(
        'accounts.President',
        on_delete=models.PROTECT,
        related_name='team',
    )

    name = models.CharField(max_length=150)

    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    foundation_year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
    upload_to='team_covers/',
    blank=True,
    null=True
)
    
    manager_name = models.CharField(
        max_length=150,
        blank=True
    )
    description = models.TextField(blank=True)
    total_titles = models.PositiveIntegerField(
        default=0
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    website = models.URLField(blank=True)

    facebook_url = models.URLField(blank=True)

    twitter_url = models.URLField(blank=True)

    youtube_url = models.URLField(blank=True)

    games_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    total_points = models.PositiveIntegerField(default=0)

    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    class Meta:
        ordering = ['name']
        unique_together = ['season', 'name']

    def __str__(self):
        return self.name


def recalculate_season_standings(season):
    """
    Recalculates points, wins, draws, losses, goals for, goals against, and games played
    for all teams in the given season based on completed matches.
    """
    teams = {team.id: team for team in season.teams.all()}

    # Reset standings
    for team in teams.values():
        team.games_played = 0
        team.wins = 0
        team.draws = 0
        team.losses = 0
        team.total_points = 0
        team.goals_for = 0
        team.goals_against = 0

    # Query completed matches
    completed_matches = season.matches.filter(status='completed')
    for match in completed_matches:
        home = teams.get(match.home_team_id)
        away = teams.get(match.away_team_id)
        if not home or not away:
            continue

        home.games_played += 1
        away.games_played += 1
        home.goals_for += match.home_score
        home.goals_against += match.away_score
        away.goals_for += match.away_score
        away.goals_against += match.home_score

        if match.home_score > match.away_score:
            home.wins += 1
            home.total_points += 3
            away.losses += 1
        elif match.away_score > match.home_score:
            away.wins += 1
            away.total_points += 3
            home.losses += 1
        else:
            home.draws += 1
            home.total_points += 1
            away.draws += 1
            away.total_points += 1

    # Save all team stats
    for team in teams.values():
        team.save()
