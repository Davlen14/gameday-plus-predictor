"""
College Football Rivalry Games Configuration
Maps team pairs to their rivalry names and trophies
"""

# Rivalry games with trophy names
RIVALRY_GAMES = {
    # Week 14 Rivalries (Rivalry Week)
    ("Ohio State", "Michigan"): {
        "name": "The Game",
        "trophy": None,
        "established": 1897
    },
    ("Michigan", "Ohio State"): {
        "name": "The Game",
        "trophy": None,
        "established": 1897
    },
    ("Clemson", "South Carolina"): {
        "name": "The Palmetto Bowl",
        "trophy": "Palmetto Trophy",
        "established": 1896
    },
    ("South Carolina", "Clemson"): {
        "name": "The Palmetto Bowl",
        "trophy": "Palmetto Trophy",
        "established": 1896
    },
    ("Kentucky", "Louisville"): {
        "name": "Battle of the Bluegrass",
        "trophy": "Governor's Cup",
        "established": 1912
    },
    ("Louisville", "Kentucky"): {
        "name": "Battle of the Bluegrass",
        "trophy": "Governor's Cup",
        "established": 1912
    },
    ("Wisconsin", "Minnesota"): {
        "name": "The Axe",
        "trophy": "Paul Bunyan's Axe",
        "established": 1890
    },
    ("Minnesota", "Wisconsin"): {
        "name": "The Axe",
        "trophy": "Paul Bunyan's Axe",
        "established": 1890
    },
    ("Oregon", "Washington"): {
        "name": "The Cascade Clash",
        "trophy": None,
        "established": 1900
    },
    ("Washington", "Oregon"): {
        "name": "The Cascade Clash",
        "trophy": None,
        "established": 1900
    },
    ("Florida State", "Florida"): {
        "name": "The Sunshine Showdown",
        "trophy": None,
        "established": 1958
    },
    ("Florida", "Florida State"): {
        "name": "The Sunshine Showdown",
        "trophy": None,
        "established": 1958
    },
    ("Virginia Tech", "Virginia"): {
        "name": "The Commonwealth Cup",
        "trophy": "Commonwealth Cup",
        "established": 1895
    },
    ("Virginia", "Virginia Tech"): {
        "name": "The Commonwealth Cup",
        "trophy": "Commonwealth Cup",
        "established": 1895
    },
    ("Alabama", "Auburn"): {
        "name": "The Iron Bowl",
        "trophy": "Foy–ODK Trophy",
        "established": 1893
    },
    ("Auburn", "Alabama"): {
        "name": "The Iron Bowl",
        "trophy": "Foy–ODK Trophy",
        "established": 1893
    },
    ("Northwestern", "Illinois"): {
        "name": "The Land of Lincoln Trophy",
        "trophy": "Land of Lincoln Trophy",
        "established": 1892
    },
    ("Illinois", "Northwestern"): {
        "name": "The Land of Lincoln Trophy",
        "trophy": "Land of Lincoln Trophy",
        "established": 1892
    },
    ("UCLA", "USC"): {
        "name": "The Crosstown Rivalry",
        "trophy": "Victory Bell",
        "established": 1929
    },
    ("USC", "UCLA"): {
        "name": "The Crosstown Rivalry",
        "trophy": "Victory Bell",
        "established": 1929
    },
    ("North Carolina", "NC State"): {
        "name": "The Tobacco Road Rivalry",
        "trophy": None,
        "established": 1894
    },
    ("NC State", "North Carolina"): {
        "name": "The Tobacco Road Rivalry",
        "trophy": None,
        "established": 1894
    },
    ("UNLV", "Nevada"): {
        "name": "Battle for Nevada",
        "trophy": "Fremont Cannon",
        "established": 1969
    },
    ("Nevada", "UNLV"): {
        "name": "Battle for Nevada",
        "trophy": "Fremont Cannon",
        "established": 1969
    },
    ("Notre Dame", "Stanford"): {
        "name": "Legends Trophy",
        "trophy": "Legends Trophy",
        "established": 1925
    },
    ("Stanford", "Notre Dame"): {
        "name": "Legends Trophy",
        "trophy": "Legends Trophy",
        "established": 1925
    },
    ("Ole Miss", "Mississippi State"): {
        "name": "The Egg Bowl",
        "trophy": "Golden Egg",
        "established": 1901
    },
    ("Mississippi State", "Ole Miss"): {
        "name": "The Egg Bowl",
        "trophy": "Golden Egg",
        "established": 1901
    },
    ("Iowa", "Nebraska"): {
        "name": "The Heroes Game",
        "trophy": "Heroes Trophy",
        "established": 1891
    },
    ("Nebraska", "Iowa"): {
        "name": "The Heroes Game",
        "trophy": "Heroes Trophy",
        "established": 1891
    },
    ("Air Force", "Colorado State"): {
        "name": "Ram–Falcon Trophy",
        "trophy": "Ram–Falcon Trophy",
        "established": 1957
    },
    ("Colorado State", "Air Force"): {
        "name": "Ram–Falcon Trophy",
        "trophy": "Ram–Falcon Trophy",
        "established": 1957
    },
    ("Georgia", "Georgia Tech"): {
        "name": "Clean, Old-Fashioned Hate",
        "trophy": "Governor's Cup",
        "established": 1893
    },
    ("Georgia Tech", "Georgia"): {
        "name": "Clean, Old-Fashioned Hate",
        "trophy": "Governor's Cup",
        "established": 1893
    },
    ("Indiana", "Purdue"): {
        "name": "The Old Oaken Bucket",
        "trophy": "Old Oaken Bucket",
        "established": 1891
    },
    ("Purdue", "Indiana"): {
        "name": "The Old Oaken Bucket",
        "trophy": "Old Oaken Bucket",
        "established": 1891
    },
    ("Texas A&M", "Texas"): {
        "name": "The Lone Star Showdown",
        "trophy": "Lone Star Showdown Trophy",
        "established": 1894
    },
    ("Texas", "Texas A&M"): {
        "name": "The Lone Star Showdown",
        "trophy": "Lone Star Showdown Trophy",
        "established": 1894
    },
    ("Arizona", "Arizona State"): {
        "name": "The Territorial Cup",
        "trophy": "Territorial Cup",
        "established": 1899
    },
    ("Arizona State", "Arizona"): {
        "name": "The Territorial Cup",
        "trophy": "Territorial Cup",
        "established": 1899
    }
}

def is_rivalry_game(team1: str, team2: str) -> bool:
    """Check if two teams have a rivalry"""
    # Normalize team names (strip whitespace, handle case)
    team1_clean = team1.strip()
    team2_clean = team2.strip()
    
    # Try exact match first
    if (team1_clean, team2_clean) in RIVALRY_GAMES:
        return True
    
    # Try case-insensitive match
    for (t1, t2), info in RIVALRY_GAMES.items():
        if (t1.lower() == team1_clean.lower() and t2.lower() == team2_clean.lower()):
            return True
    
    return False

def get_rivalry_info(team1: str, team2: str) -> dict:
    """Get rivalry information for two teams"""
    # Normalize team names
    team1_clean = team1.strip()
    team2_clean = team2.strip()
    
    # Try exact match first
    result = RIVALRY_GAMES.get((team1_clean, team2_clean))
    if result:
        # Add the normalized name for display
        result['name_display'] = f"{team1_clean} vs {team2_clean}"
        return result
    
    # Try case-insensitive match
    for (t1, t2), info in RIVALRY_GAMES.items():
        if (t1.lower() == team1_clean.lower() and t2.lower() == team2_clean.lower()):
            # Add the normalized name for display
            rivalry_info = info.copy()
            rivalry_info['name_display'] = f"{team1_clean} vs {team2_clean}"
            return rivalry_info
    
    return None
