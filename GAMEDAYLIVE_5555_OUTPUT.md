# Gamedaylive Page Output Comparison

---

## Port 5555 (app_master.py)
**URL:** http://localhost:5555/gamedaylive

Away Team
Old Dominion
-
vs
Home Team
South Florida
-
Upcoming
·
Camping World Stadium
Wed, Dec 17, 5:00 PM EST
Lines
South -3
O/U: 53.5
PREV

0
Days
:
19
Hrs
:
58
Min
:
04
Sec
10
10
20
20
30
30
40
40
50
50
40
40
30
30
20
20
10
10
Away Team
-
9-3
Old Dominion
VS
Regular Season
Home Team
-
9-3
South Florida
Season Leaders
Old Dominion
Passing
-
- YDS
Rushing
-
- YDS
Receiving
-
- YDS
South Florida
Passing
-
- YDS
Rushing
-
- YDS
Receiving
-
- YDS
Last 5 Games
Old Dominion
No recent games
South Florida
No recent games

Preview
Betting
History
Win Probability
Away
Home
50%
50%
Lines
DK
-3
53.5
BV
-3
53.5
ESPN
-3
53.5
Head Coaches

Ricky Rahne
29-33
vs Ranked: -

Alex Golesh
23-15
vs Ranked: -
Head-to-Head
-
All-Time
-
Offensive Stats
32.7
Points/Game
43.0
461
Yards/Game
501
40.9%
3rd Down
47.9%
-
Red Zone
-
Defensive Stats
19.3
Pts Allowed
23.3
2.9
Sacks/Game
2.4
1.8
TO/Game
2.0
Advanced Metrics
3.5
FPI
12.3
6.3
SP+ Overall
14.3
32.0
SP+ Off
39.8
24.8
SP+ Def
25.4
Talent Pipeline
#102
Latest Class
#65
-
Talent Rank
-
-
Draft Picks (Career)
-
Clutch Performance
13-15
1-Score Games
4-3
0
Comeback Wins
0
22-18
Conf Record
14-10
Game Info
Camping World Stadium
Wed, Dec 17, 5:00 PM EST
TBD
G+
Powered by
GAMEDAY+

---

## Port 5002 (app.py - Full Stack)
**URL:** http://localhost:5002/gamedaylive

Away Team
Old Dominion
-
vs
Home Team
South Florida
-
Game Time!
·
TBD
Mon, Jan 20, 3:00 PM EST
Lines
South -3
O/U: 53.5
PREV

0
Days
:
0
Hrs
:
0
Min
:
0
Sec
10
10
20
20
30
30
40
40
50
50
40
40
30
30
20
20
10
10
Away Team
-
9-3
Old Dominion
VS
Regular Season
Home Team
-
9-3
South Florida
Season Leaders
Old Dominion
Passing
-
- YDS
Rushing
-
- YDS
Receiving
-
- YDS
South Florida
Passing
-
- YDS
Rushing
-
- YDS
Receiving
-
- YDS
Last 5 Games
Old Dominion
No recent games
South Florida
No recent games

Preview
Betting
History
Win Probability
Away
Home
50%
50%
Lines
DK
-3
53.5
BV
-3
53.5
ESPN
-3
53.5
Head Coaches

Ricky Rahne
29-33
vs Ranked: -

Alex Golesh
23-15
vs Ranked: -
Head-to-Head
-
All-Time
-
Offensive Stats
-
Points/Game
-
-
Yards/Game
-
-
3rd Down
-
-
Red Zone
-
Defensive Stats
-
Pts Allowed
-
-
Sacks/Game
-
-
TO/Game
-
Advanced Metrics
3.5
FPI
12.3
-
SP+ Overall
-
-
SP+ Off
-
-
SP+ Def
-
Talent Pipeline
-
Latest Class
-
-
Talent Rank
-
-
Draft Picks (Career)
-
Clutch Performance
-
1-Score Games
-
-
Comeback Wins
-
-
Conf Record
-
Game Info
TBD
Mon, Jan 20, 3:00 PM EST
TBD

---

## ❌ Data 5555 Has That 5002 Is Missing

| Category | Stat | 5555 Value | 5002 Value |
|----------|------|------------|------------|
| ❌ Offensive Stats | Points/Game | 32.7 vs 43.0 | - vs - |
| ❌ Offensive Stats | Yards/Game | 461 vs 501 | - vs - |
| ❌ Offensive Stats | 3rd Down | 40.9% vs 47.9% | - vs - |
| ❌ Defensive Stats | Pts Allowed | 19.3 vs 23.3 | - vs - |
| ❌ Defensive Stats | Sacks/Game | 2.9 vs 2.4 | - vs - |
| ❌ Defensive Stats | TO/Game | 1.8 vs 2.0 | - vs - |
| ❌ Advanced Metrics | SP+ Overall | 6.3 vs 14.3 | - vs - |
| ❌ Advanced Metrics | SP+ Off | 32.0 vs 39.8 | - vs - |
| ❌ Advanced Metrics | SP+ Def | 24.8 vs 25.4 | - vs - |
| ❌ Talent Pipeline | Latest Class | #102 vs #65 | - vs - |
| ❌ Clutch Performance | 1-Score Games | 13-15 vs 4-3 | - vs - |
| ❌ Clutch Performance | Comeback Wins | 0 vs 0 | - vs - |
| ❌ Clutch Performance | Conf Record | 22-18 vs 14-10 | - vs - |

---

## 🤖 AI FIX PROMPT

```
The gamedaylive page on port 5002 (app.py) is missing team statistics data that port 5555 (app_master.py) correctly displays.

PROBLEM:
- Port 5555 shows actual stats (Points/Game, Yards/Game, 3rd Down %, Pts Allowed, Sacks/Game, TO/Game, SP+ metrics, Latest Class rank, 1-Score Games, Comeback Wins, Conf Record)
- Port 5002 shows dashes (-) for all these same fields

TASK:
1. Find why app.py (port 5002) is not returning team stats data for the gamedaylive page
2. Compare the API endpoint or data source used by app_master.py vs app.py for these stats
3. The data exists in the database (proven by 5555 working) - app.py is likely not querying it or not passing it to the template
4. Check the /api/upcoming-games endpoint or whichever endpoint feeds the gamedaylive template
5. Ensure offensive stats, defensive stats, advanced metrics, talent pipeline, and clutch performance data are being fetched and returned

FILES TO CHECK:
- app.py (port 5002 routes)
- app_master.py (port 5555 routes - this one works)
- templates/gamedaylive.html (shared template)
- Any API endpoints that provide game/team stats
```
