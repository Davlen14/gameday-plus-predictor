#!/usr/bin/env python3
"""
Fetch comprehensive data for all G5 coaches and populate database
Uses CFBD GraphQL API to get complete career stats
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from urllib import request, error
from typing import Dict, List

DB_FILE = Path("instance/coaches_master.db")
GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

def query_gql(q: str, variables: Dict = None) -> Dict:
    """Execute GraphQL query"""
    payload = {"query": q}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        GRAPHQL_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return json.loads(body).get("data", {}) or {}
    except error.HTTPError as exc:
        print(f"⚠️  HTTP error: {exc}")
    except Exception as exc:
        print(f"⚠️  Query error: {exc}")
    return {}


def fetch_coach_career_games(coach_name: str) -> Dict:
    """Fetch all career games for a coach"""
    # Query for coach's career
    q = f'''{{
        coach(where: {{
            firstName_lastName_school: {{_ilike: "%{coach_name}%"}}
        }}) {{
            firstName
            lastName
            school
            seasons
        }}
    }}'''
    
    coaches = query_gql(q).get("coach", [])
    
    if not coaches:
        print(f"  ⚠️  No data found for {coach_name}")
        return {}
    
    # Get first match
    coach = coaches[0]
    school = coach.get("school")
    seasons = coach.get("seasons", [])
    
    if not seasons:
        print(f"  ⚠️  No seasons found for {coach_name}")
        return {}
    
    # Calculate stats from seasons
    total_games = 0
    total_wins = 0
    
    for season in seasons:
        games = season.get("games", 0)
        wins = season.get("wins", 0)
        total_games += games
        total_wins += wins
    
    total_losses = total_games - total_wins
    win_pct = total_wins / total_games if total_games > 0 else 0.0
    
    return {
        "career_record": f"{total_wins}-{total_losses}",
        "career_win_pct": round(win_pct, 3),
        "total_games": total_games,
        "school": school
    }


def fetch_coach_seasons(coach_name: str, school: str) -> List[Dict]:
    """Fetch season-by-season data for coach"""
    q = f'''{{
        coach(where: {{
            firstName_lastName_school: {{_ilike: "%{coach_name}%"}},
            school: {{_eq: "{school}"}}
        }}) {{
            firstName
            lastName
            school
            seasons {{
                year
                games
                wins
                losses
                ties
                sp
                srs
                apRank
                postseasonRank
            }}
        }}
    }}'''
    
    result = query_gql(q)
    coaches = result.get("coach", [])
    
    if not coaches:
        return []
    
    return coaches[0].get("seasons", [])


def update_coach_in_db(coach_id: int, coach_name: str, school: str):
    """Update a single coach with comprehensive data"""
    print(f"\n  Fetching data for {coach_name} ({school})...")
    
    # Fetch career stats
    career_stats = fetch_coach_career_games(coach_name)
    
    if not career_stats:
        print(f"    ⊙ No CFBD data available for {coach_name}")
        return False
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Update coach record
        cursor.execute("""
            UPDATE coaches 
            SET career_record = ?,
                career_win_pct = ?,
                total_games = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            career_stats["career_record"],
            career_stats["career_win_pct"],
            career_stats["total_games"],
            datetime.now().isoformat(),
            coach_id
        ))
        
        # Fetch and insert season data
        seasons = fetch_coach_seasons(coach_name, school)
        
        if seasons:
            print(f"    → Found {len(seasons)} seasons")
            for season in seasons:
                cursor.execute("""
                    INSERT OR REPLACE INTO season_analytics (
                        coach_id, season, games, wins, losses, win_pct,
                        sp_rating, srs_rating, ap_rank, postseason_rank
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    coach_id,
                    season.get("year"),
                    season.get("games", 0),
                    season.get("wins", 0),
                    season.get("losses", 0),
                    season.get("wins", 0) / season.get("games", 1) if season.get("games", 0) > 0 else 0.0,
                    season.get("sp"),
                    season.get("srs"),
                    season.get("apRank"),
                    season.get("postseasonRank")
                ))
        
        conn.commit()
        print(f"    ✓ Updated {coach_name}: {career_stats['career_record']} ({career_stats['total_games']} games)")
        return True
        
    except Exception as e:
        print(f"    ⚠️  Error updating {coach_name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def main():
    print("="*60)
    print("COMPREHENSIVE COACH DATA FETCH")
    print("="*60)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get all coaches that need data
    cursor.execute("""
        SELECT id, name, current_school 
        FROM coaches 
        WHERE career_record = '0-0' OR total_games = 0
        ORDER BY current_school
    """)
    
    coaches_to_update = cursor.fetchall()
    conn.close()
    
    print(f"\nFound {len(coaches_to_update)} coaches needing comprehensive data\n")
    
    updated = 0
    failed = 0
    
    for coach_id, coach_name, school in coaches_to_update:
        try:
            if update_coach_in_db(coach_id, coach_name, school):
                updated += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ⚠️  Failed to process {coach_name}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✓ Successfully updated: {updated} coaches")
    print(f"⚠️  Failed/No data: {failed} coaches")
    print(f"\nTotal coaches in database:")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM coaches")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM coaches WHERE total_games > 0")
    with_data = cursor.fetchone()[0]
    conn.close()
    
    print(f"  Total: {total}")
    print(f"  With comprehensive data: {with_data}")
    print(f"  Still need data: {total - with_data}")


if __name__ == "__main__":
    main()
