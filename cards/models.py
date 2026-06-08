from django.db import models


class SecretCard(models.Model):
    class CardType(models.TextChoices):
        ONE_V_ONE = '1v1_mode', '1v1 Mode'
        DOUBLE_GOALS = 'double_goals', 'Double Goals'
        INSTANT_PENALTY = 'instant_penalty', 'Instant Penalty'
        REMOVE_OPPONENT = 'remove_opponent', 'Remove Opponent'

    card_type = models.CharField(max_length=30, choices=CardType.choices)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_card_type_display()


class CardActivation(models.Model):
    match = models.ForeignKey(
        'matches.Match',
        on_delete=models.CASCADE,
        related_name='card_activations',
    )
    activating_team = models.ForeignKey(
        'league.Team',
        on_delete=models.CASCADE,
        related_name='card_activations',
    )
    card = models.ForeignKey(SecretCard, on_delete=models.CASCADE, related_name='activations')
    activation_minute = models.PositiveSmallIntegerField()
    is_exhausted = models.BooleanField(default=False)

    class Meta:
        ordering = ['match', 'activation_minute']

    def __str__(self):
        return f'{self.card} at {self.activation_minute} min'
