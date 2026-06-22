from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(models.Model):
    class Role(models.TextChoices):
        PRESIDENT = 'president', 'President'
        PLAYER = 'player', 'Player'
        FAN = 'fan', 'Fan'
        ADMIN = 'admin', 'Admin'

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)

    def __str__(self):
        return f'{self.name} ({self.get_role_display()})'


class President(User):
    social_media_channel = models.URLField(blank=True)


class Player(User):
    class Position(models.TextChoices):
        GOALKEEPER = 'gk', 'Goalkeeper'
        DEFENDER = 'def', 'Defender'
        MIDFIELDER = 'mid', 'Midfielder'
        FORWARD = 'fwd', 'Forward'

    class DraftStatus(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        DRAFTED = 'drafted', 'Drafted'
        RESERVE = 'reserve', 'Reserve'

    position = models.CharField(max_length=10, choices=Position.choices)
    draft_status = models.CharField(
        max_length=20,
        choices=DraftStatus.choices,
        default=DraftStatus.AVAILABLE,
    )
    skill_rating = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    profile_image = models.ImageField(
        upload_to='player_profiles/',
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Player bio or description displayed on the profile page.',
    )
    current_team = models.ForeignKey(
        'league.Team',
        on_delete=models.SET_NULL,
        related_name='players',
        blank=True,
        null=True,
    )


class PlayerStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    mvp_awards = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_cards = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'player stats'

    def __str__(self):
        return f'{self.player.name} stats'
