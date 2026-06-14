# Pitch Prime League (PPL) Web Application

This project is a modular Django application designed for a football league (specifically tailored for modern formats like "Kings League" featuring wildcard mechanics). Each domain owns its own models, migrations, views, and routing.

---

## 🚀 Installed Apps & Core Domains

- `core`: Homepage, shared layouts, and template shells.
- `accounts`: User profiles for Presidents, Players, and Player Stats.
- `league`: League, Season, and Team hierarchy (including dynamic standings).
- `matches`: Fixtures, completed results, match details, and timeline events (goals, cards, penalties).
- `cards`: Secret card catalog and card activation logs.

---

## 🗺️ Routing & Views Architecture

Main URL routing is controlled in [primeleague/urls.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/primeleague/urls.py) and distributed to modular app-level URL configs:

### 1. League App Routing (`/league/` -> [league/urls.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/league/urls.py))
- **Season List** (`/league/`): Displays all season competition cycles. Bound to `views.season_list`.
- **Standings Table** (`/league/standings/<int:season_id>/`): Displays the current points table for a specific season. Bound to `views.standings_table`.

### 2. Matches App Routing (`/matches/` -> [matches/urls.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/matches/urls.py))
- **Fixtures List** (`/matches/fixtures/`): Lists all upcoming or live matches in the league. Bound to `views.fixture_list`.
- **Results List** (`/matches/results/`): Lists all completed matches. Bound to `views.result_list`.
- **Match Details** (`/matches/<int:pk>/`): Renders a detailed match timeline showing goals, cards, penalties, and secret card activations. Bound to `views.match_detail`.

### 3. Accounts App Routing (`/accounts/` -> [accounts/urls.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/accounts/urls.py))
- **Players List** (`/accounts/players/`): Lists all players in the league, showing their draft status and skill rating. Bound to `views.player_list`.
- **Player Profile** (`/accounts/players/<int:pk>/`): Shows a single player's details, team history, and player stats. Bound to `views.player_detail`.

---

## 📈 Dynamic Standings & Match Recalculation

To ensure the standings table remains consistent, PPL computes team statistics dynamically rather than relying on manual updates.

### 1. Extended Team Statistics
The [Team](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/league/models.py#L32) model is extended to store:
- `games_played`: Total completed matches played.
- `wins`, `draws`, `losses`: Overall match outcomes.
- `goals_for` / `goals_against`: Total goals scored and conceded.
- `total_points`: Computed points (3 points for a win, 1 for a draw, 0 for a loss).

### 2. Recalculation Engine (`recalculate_season_standings`)
Implemented in [league/models.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/league/models.py#L55), this utility function:
1. Fetches all teams registered in the given season.
2. Resets all standing fields (`games_played`, `wins`, `draws`, `losses`, `goals_for`, `goals_against`, `total_points`) to `0`.
3. Queries all matches belonging to the season that have `status = 'completed'`.
4. Loops through these matches, allocating wins, draws, losses, points, and goals to the respective home and away teams.
5. Saves all team profiles in a database transaction.

### 3. Automated Event Triggers
Standings are updated in real-time through overridden methods on the [Match](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/matches/models.py#L4) model in [matches/models.py](file:///c:/Users/echoe/OneDrive/Documents/GitHub/Pitch-prime-league/matches/models.py):
- **On Save**: Whenever a Match is saved (created or updated), `recalculate_season_standings(self.season)` is triggered automatically. This handles scores changing, match status changing (e.g. from `live` to `completed`), or goals being edited.
- **On Delete**: When a Match is deleted, `recalculate_season_standings(season)` is executed before completion, ensuring the deleted match's score is removed from the standings.

---

## 🛠️ How to Set Up and Run

### 1. Virtual Environment & Requirements
Ensure your Python environment is set up and active:
```powershell
# Create venv if not done
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 2. Apply Migrations
Execute Django migrations to prepare the database schema:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 3. Verification & Checks
Run Django's system check to verify everything is configured correctly:
```powershell
python manage.py check
```

You can verify the recalculation logic using the provided test script in the scratch directory:
```powershell
python C:\Users\echoe\.gemini\antigravity-ide\brain\18a9010f-435d-4ab6-a031-62643802bea9\scratch\test_recalc.py
```

### 4. Run Server
Launch the development server:
```powershell
python manage.py runserver
```
