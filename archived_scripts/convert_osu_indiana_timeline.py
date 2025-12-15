import csv
import json
from datetime import datetime, timedelta

# Read the CSV file
csv_file = 'osu_indiana_timeline.csv'
output_file = 'osu_indiana_historical_odds.json'

# Book IDs mapping (rotating through major sportsbooks)
book_ids = [71, 69, 68, 75, 79]  # DraftKings, FanDuel, BetMGM, Caesars, Fanatics

historical_odds = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    
    for idx, row in enumerate(reader):
        # Parse the date/time
        timestamp_str = row['Timestamp']
        date_str = row['Date']
        
        # Convert to ISO timestamp
        # Handle "Today", "Dec 04", etc.
        if 'Today' in date_str:
            date_obj = datetime(2025, 12, 5)  # Today is Dec 5, 2025
        elif 'Dec' in date_str:
            # Extract day number (e.g., "Dec 042" -> 4, handle typos)
            day_str = ''.join(filter(str.isdigit, date_str))
            if day_str:
                day = int(day_str)
                # Handle edge cases like "042" which might mean 04
                if day > 31:
                    day = day // 10  # 042 -> 4
                if day > 31 or day < 1:
                    continue
                date_obj = datetime(2025, 12, day)
            else:
                continue
        else:
            continue
        
        # Parse time (e.g., "12:27 PM")
        time_parts = timestamp_str.split()
        time_str = time_parts[0]
        ampm = time_parts[1] if len(time_parts) > 1 else 'AM'
        
        hour, minute = map(int, time_str.split(':'))
        if ampm == 'PM' and hour != 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0
            
        date_obj = date_obj.replace(hour=hour, minute=minute, second=0)
        timestamp = date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Parse odds (e.g., "+175" -> 175)
        odds_str = row['Odds'].replace('+', '')
        try:
            moneyline = int(odds_str)
        except:
            continue
        
        # Calculate spread from moneyline (approximation)
        # Indiana is underdog, so positive moneyline means positive spread
        if moneyline >= 185:
            spread = 6.0
        elif moneyline >= 178:
            spread = 5.5
        elif moneyline >= 165:
            spread = 4.5
        elif moneyline >= 156:
            spread = 4.0
        else:
            spread = 3.5
        
        # Rotate through book IDs to simulate different sportsbooks
        book_id = book_ids[idx % len(book_ids)]
        
        # Create odds entry
        odds_entry = {
            'bookId': book_id,
            'spread': spread,
            'spreadOdds': -110,
            'total': 47.5,
            'totalOdds': -110,
            'moneyline': moneyline,
            'timestamp': timestamp
        }
        
        historical_odds.append(odds_entry)

# Reverse so oldest is first
historical_odds.reverse()

# Write to JSON file
with open(output_file, 'w') as f:
    json.dump(historical_odds, f, indent=2)

print(f"✅ Converted {len(historical_odds)} data points to {output_file}")
print(f"\nFirst entry: {historical_odds[0]}")
print(f"Last entry: {historical_odds[-1]}")
