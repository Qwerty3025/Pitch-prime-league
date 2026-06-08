# Ballers League Web Application

This project uses a modular Django app structure so each domain owns its own models, migrations, and future business logic.

## Installed Apps

The local project apps currently installed in `primeleague/settings.py` are:

- `core`: Homepage and shared project-level views.
- `accounts`: User domain models for presidents, players, and player stats.
- `league`: League, season, and team structure.
- `matches`: Fixtures, live match state, and match timeline events.
- `cards`: Wildcard card catalog and card activation records.

## App Structure

```text
Pitch-prime-league/
├── accounts/
│   ├── models.py        # User, President, Player, PlayerStats
│   └── migrations/
├── cards/
│   ├── models.py        # SecretCard, CardActivation
│   └── migrations/
├── core/
│   ├── views.py         # Homepage view
│   ├── urls.py          # Homepage route
│   └── migrations/      # Removes old centralized domain models
├── league/
│   ├── models.py        # League, Season, Team
│   └── migrations/
├── matches/
│   ├── models.py        # Match, MatchEvent, GoalEvent, CardEvent, PenaltyEvent
│   └── migrations/
├── primeleague/
│   ├── settings.py
│   └── urls.py
├── static/
└── templates/
```

## Domain Boundaries

### `accounts`

Owns identity and profile-related data.

- `User`: Base profile entity with `name`, `email`, and `role`.
- `President`: Specialized user for team presidents and content creators.
- `Player`: Specialized user for athletes, including position, draft status, skill rating, and current team.
- `PlayerStats`: One-to-one statistics record for a player.

### `league`

Owns the competition hierarchy.

- `League`: Top-level league container.
- `Season`: A specific league tournament cycle.
- `Team`: A franchise in a season with one president and many players.

### `matches`

Owns fixture state and match events.

- `Match`: A scheduled fixture between two teams.
- `MatchEvent`: Base timeline event for a match.
- `GoalEvent`: Specialized goal event.
- `CardEvent`: Specialized yellow/red card event.
- `PenaltyEvent`: Specialized penalty event.

### `cards`

Owns wildcard mechanics.

- `SecretCard`: Card catalog, such as `1v1 Mode`, `Double Goals`, and `Instant Penalty`.
- `CardActivation`: Tracks when a card is activated in a match and by which team.

## Model Relationships

- A `League` has many `Season` records.
- A `Season` has many `Team` and `Match` records.
- A `Team` has one `President`.
- A `Team` has many `Player` records through `Player.current_team`.
- A `Player` has one `PlayerStats` record.
- A `Match` has many `MatchEvent` records.
- A `Match` has many `CardActivation` records.

## Migration Notes

The domain models were moved out of `core` into dedicated apps. The new migrations create tables for `accounts`, `league`, `matches`, and `cards`, while `core` now contains a migration that removes the old centralized model tables.

Run migrations with:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```
