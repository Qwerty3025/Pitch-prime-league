from django.db import models


class League(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Season(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    standings_table = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-season_number']
        unique_together = ['league', 'season_number']

    def __str__(self):
        return f'{self.league.name} Season {self.season_number}'


class Team(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='teams')
    president = models.OneToOneField(
        'accounts.President',
        on_delete=models.PROTECT,
        related_name='team',
    )
    name = models.CharField(max_length=150)
    logo_url = models.URLField(blank=True)
    total_points = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        unique_together = ['season', 'name']

    def __str__(self):
        return self.name
