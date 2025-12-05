import json
from datetime import datetime

def get_week_date(season, week):
    """Convert season and week to approximate date"""
    # Season starts in late August/early September
    start_month = 8 if week <= 1 else 8
    start_day = 25 + (week - 1) * 7
    
    if start_day > 31:
        months_over = (start_day - 1) // 30
        start_month += months_over
        start_day = start_day - (months_over * 30)
    
    if start_month > 12:
        start_month = start_month - 12
        season += 1
    
    return f"Date.UTC({season}, {start_month - 1}, {start_day})"

# Load all school data
schools = {
    'notre_dame': json.load(open('kelly_notre_dame.json')),
    'cincinnati': json.load(open('kelly_cincinnati.json')),
    'lsu': None  # Will use existing LSU data
}

all_rankings = []

# Process Notre Dame (2010-2021)
nd_rankings = schools['notre_dame'].get('rankings', [])
for r in nd_rankings:
    if 2010 <= r['poll']['season'] <= 2021:
        week = r['poll']['week']
        season = r['poll']['season']
        rank = r['rank']
        date = get_week_date(season, week)
        all_rankings.append(f"            [{date}, {rank}],  // Notre Dame {season} Week {week}")

# Process Cincinnati (2006-2009)
cin_rankings = schools['cincinnati'].get('rankings', [])
for r in cin_rankings:
    if 2006 <= r['poll']['season'] <= 2009:
        week = r['poll']['week']
        season = r['poll']['season']
        rank = r['rank']
        date = get_week_date(season, week)
        all_rankings.append(f"            [{date}, {rank}],  // Cincinnati {season} Week {week}")

# Sort by date and print
all_rankings.sort()
print("// Complete Brian Kelly Career Rankings Data")
print("const rankingsData = [")
for r in all_rankings:
    print(r)
print("            // LSU data continues...")
print("];")
