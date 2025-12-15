# Coach Career Summary Generator

Generate comprehensive JSON summaries of any coach's career for use in React components.

## 📁 Files

- **`generate_coach_summary_json.py`** - Main script to generate JSON summaries
- **`analyze_coach.py`** - Terminal-based analysis tool
- **`matt_campbell_summary.json`** - Example generated summary (Matt Campbell)
- **`CoachSummaryExample.tsx`** - Example React components

## 🚀 Quick Start

### Generate a JSON Summary

```bash
# Generate summary for Matt Campbell
python3 generate_coach_summary_json.py enhanced_coaches_v2/matt_campbell_master_v2.json

# Output: matt_campbell_summary.json

# Generate for any coach with custom output name
python3 generate_coach_summary_json.py enhanced_coaches_v2/lane_kiffin_master.json lane_kiffin.json
```

### Terminal Analysis (Human-Readable)

```bash
# View detailed analysis in terminal
python3 analyze_coach.py enhanced_coaches_v2/matt_campbell_master_v2.json

# Save to text file
python3 analyze_coach.py enhanced_coaches_v2/matt_campbell_master_v2.json > analysis.txt
```

## 📊 JSON Structure

The generated JSON includes:

```json
{
  "coach_name": "Matt Campbell",
  "headshot": "https://...",
  "schools": ["Toledo", "Iowa State"],
  "generated": "2025-12-06T10:29:06.695737",

  "career_stats": {
    "record": "122-79",
    "wins": 122,
    "losses": 79,
    "total_games": 201,
    "win_pct": 60.7,
    "points_per_game": 30.9,
    "opp_points_per_game": 25.0,
    "point_differential": 5.9
  },

  "stints": [
    {
      "school": "Toledo",
      "start_year": 2011,
      "end_year": 2015,
      "record": "47-20",
      "win_pct": 70.1,
      "games": 67
    },
    {
      "school": "Iowa State",
      "start_year": 2016,
      "end_year": 2025,
      "record": "75-59",
      "win_pct": 56.0,
      "games": 134
    }
  ],

  "game_analysis": {
    "home": { "games": 97, "wins": 65, "losses": 32, "win_pct": 67.0 },
    "away": { "games": 82, "wins": 46, "losses": 36, "win_pct": 56.1 },
    "neutral": { "games": 22, "wins": 11, "losses": 11, "win_pct": 50.0 },
    "close_games": { "total": 91, "wins": 44, "losses": 47, "win_pct": 48.4 }
  },

  "signature_wins": [
    {
      "season": 2017,
      "week": 6,
      "opponent": "Oklahoma",
      "context": "Upset of #3 ranked Sooners",
      "impact": "Program-defining moment"
    }
  ],

  "season_progression": [
    {
      "year": 2020,
      "games": 13,
      "wins": 10,
      "losses": 3,
      "win_pct": 76.9,
      "points_per_game": 33.0,
      "opp_points_per_game": 21.1
    }
  ],

  "nfl_pipeline": {
    "total_picks": 15,
    "players": [
      {
        "name": "Breece Hall",
        "year": 2022,
        "round": 2,
        "team": "New York Jets"
      }
    ]
  },

  "talent_ratings": [
    { "year": 2025, "school": "Iowa State", "rating": 648.93 }
  ],

  "ai_narrative": "AI-generated career summary...",
  "nfl_draft_picks": 15
}
```

## 🎨 React Component Usage

### Import the JSON

```tsx
import coachSummary from './matt_campbell_summary.json';
```

### Use in Components

```tsx
// Display career stats
<div>
  <h2>{coachSummary.coach_name}</h2>
  <p>Record: {coachSummary.career_stats.record}</p>
  <p>Win %: {coachSummary.career_stats.win_pct.toFixed(1)}%</p>
</div>

// Map over signature wins
{coachSummary.signature_wins.map((win, idx) => (
  <div key={idx}>
    {win.season} Week {win.week}: vs {win.opponent}
  </div>
))}

// Display season progression
{coachSummary.season_progression.map(season => (
  <div key={season.year}>
    {season.year}: {season.wins}-{season.losses}
  </div>
))}
```

See `CoachSummaryExample.tsx` for complete component examples.

## 📈 Matt Campbell Summary Highlights

**Career:** 122-79 (60.7%) over 201 games

**Toledo (2011-2015):** 47-20 (70.1%)
- 2x MAC Championships
- Upset of Arkansas (2015)

**Iowa State (2016-2025):** 75-59 (56.0%)
- Transformed struggling program into Big 12 contender
- Signature wins: #3 Oklahoma (2017), Oregon (Fiesta Bowl 2020)
- 15 NFL Draft picks including Breece Hall, Brock Purdy

**Performance:**
- 30.9 PPG, 25.0 opp PPG (+5.9 differential)
- Home: 65-32 (67.0%)
- Away: 46-36 (56.1%)
- Close games: 44-47 (48.4%)

## 🤖 AI Enhancement

The script uses Gemini AI to generate narrative summaries. If the API quota is exceeded, it falls back to a standard summary.

## 🔧 Generate for Other Coaches

Works with any coach in your `enhanced_coaches_v2/` folder:

```bash
# Find available coaches
ls enhanced_coaches_v2/*_master*.json

# Generate summaries
python3 generate_coach_summary_json.py enhanced_coaches_v2/lane_kiffin_master.json
python3 generate_coach_summary_json.py enhanced_coaches_v2/kirby_smart_master.json
python3 generate_coach_summary_json.py enhanced_coaches_v2/nick_saban_master.json
```

## 📦 TypeScript Types

See `CoachSummaryExample.tsx` for complete TypeScript interface definition.

```tsx
interface CoachSummary {
  coach_name: string;
  headshot: string;
  schools: string[];
  career_stats: { ... };
  stints: Array<{ ... }>;
  // ... full type definition in example file
}
```

## ✨ Ready to Use!

The JSON files are ready to import directly into your React components. Copy them to your `frontend/src/data/` directory and import as needed.
