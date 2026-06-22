from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Match(models.Model):
    class Status(models.TextChoices):
        UPCOMING = 'upcoming', 'Upcoming'
        LIVE = 'live', 'Live'
        COMPLETED = 'completed', 'Completed'

    season = models.ForeignKey('league.Season', on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(
        'league.Team',
        on_delete=models.CASCADE,
        related_name='home_matches',
    )
    away_team = models.ForeignKey(
        'league.Team',
        on_delete=models.CASCADE,
        related_name='away_matches',
    )
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)

    def get_winner(self):
        if self.status != self.Status.COMPLETED:
            return None
        if self.home_score > self.away_score:
            return self.home_team
        if self.away_score > self.home_score:
            return self.away_team
        return None  # Represents a draw

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f'{self.home_team.name} vs {self.away_team.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from league.models import recalculate_season_standings
        recalculate_season_standings(self.season)

    def delete(self, *args, **kwargs):
        season = self.season
        super().delete(*args, **kwargs)
        from league.models import recalculate_season_standings
        recalculate_season_standings(season)


class MatchEvent(models.Model):
    class EventType(models.TextChoices):
        GOAL = 'goal', 'Goal'
        CARD = 'card', 'Card'
        PENALTY = 'penalty', 'Penalty'

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    timestamp_minute = models.PositiveSmallIntegerField()
    acting_team = models.ForeignKey(
        'league.Team',
        on_delete=models.SET_NULL,
        related_name='match_events',
        blank=True,
        null=True,
    )
    associated_player = models.ForeignKey(
        'accounts.Player',
        on_delete=models.SET_NULL,
        related_name='match_events',
        blank=True,
        null=True,
    )
    event_type = models.CharField(max_length=20, choices=EventType.choices)

    class Meta:
        ordering = ['match', 'timestamp_minute']

    def __str__(self):
        return f'{self.match} - {self.timestamp_minute} min'


class GoalEvent(MatchEvent):
    is_own_goal = models.BooleanField(default=False)
    is_assisted = models.BooleanField(default=False)
    assistant_player = models.ForeignKey(
        'accounts.Player',
        on_delete=models.SET_NULL,
        related_name='assisted_goal_events',
        blank=True,
        null=True,
    )


class CardEvent(MatchEvent):
    class CardColor(models.TextChoices):
        YELLOW = 'yellow', 'Yellow'
        RED = 'red', 'Red'

    card_color = models.CharField(max_length=10, choices=CardColor.choices)
    duration_minutes = models.PositiveSmallIntegerField(blank=True, null=True)


class PenaltyEvent(MatchEvent):
    class PenaltyType(models.TextChoices):
        IN_GAME = 'in_game', 'In Game'
        SHOOTOUT = 'shootout', 'Shootout'

    is_scored = models.BooleanField(default=False)
    penalty_type = models.CharField(max_length=20, choices=PenaltyType.choices)   


class MatchStats(models.Model):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name='stats'
    )

    home_possession = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    away_possession = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    home_shots = models.PositiveIntegerField(default=0)
    away_shots = models.PositiveIntegerField(default=0)

    home_shots_on_target = models.PositiveIntegerField(default=0)
    away_shots_on_target = models.PositiveIntegerField(default=0)

    home_touches = models.PositiveIntegerField(default=0)
    away_touches = models.PositiveIntegerField(default=0)

    home_passes = models.PositiveIntegerField(default=0)
    away_passes = models.PositiveIntegerField(default=0)

    home_tackles = models.PositiveIntegerField(default=0)
    away_tackles = models.PositiveIntegerField(default=0)

    home_clearances = models.PositiveIntegerField(default=0)
    away_clearances = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats - {self.match}"
    


@receiver(post_save, sender=Match)
def create_match_stats(sender, instance, created, **kwargs):

    if created:
        MatchStats.objects.create(
            match=instance
        ) 




















