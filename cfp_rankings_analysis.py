#!/usr/bin/env python3
"""
CFP RANKINGS TRAJECTORY ANALYZER
Quick analysis of just the rankings data for all 12 CFP teams
"""

import sqlite3
from pathlib import Path

def analyze_cfp_rankings():
    """Analyze rankings trajectory for all CFP teams"""
    
    db_path = Path('instance/playoff_team_analysis.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cfp_teams = [
        'Indiana', 'Ohio State', 'Georgia', 'Texas Tech',  # Top 4 seeds
        'Oregon', 'Ole Miss', 'Texas A&M', 'Oklahoma',    # Seeds 5-8
        'Alabama', 'Miami', 'Tulane', 'James Madison'     # Seeds 9-12
    ]
    
    print("🏆 CFP TEAMS RANKINGS TRAJECTORY ANALYSIS")
    print("=" * 80)
    
    for team in cfp_teams:
        print(f"\n📈 {team.upper()} RANKINGS HISTORY:")
        
        # Team rankings (AP/Coaches/Playoff)
        rankings_query = """
        SELECT tr.season, tr.week, tr.ap_rank, tr.coaches_rank, tr.playoff_rank
        FROM team_rankings tr 
        JOIN teams t ON tr.team_id = t.id 
        WHERE t.school = ?
        ORDER BY tr.season DESC, tr.week DESC
        LIMIT 20
        """
        
        rankings = cursor.execute(rankings_query, [team]).fetchall()
        
        if rankings:
            print(f"   {'Season':6} {'Week':4} {'AP':4} {'Coaches':8} {'CFP':4}")
            print(f"   {'-'*35}")
            
            for season, week, ap_rank, coaches_rank, playoff_rank in rankings:
                ap_display = f"#{ap_rank}" if ap_rank else "NR"
                coaches_display = f"#{coaches_rank}" if coaches_rank else "NR"
                playoff_display = f"#{playoff_rank}" if playoff_rank else "NR"
                print(f"   {season:6} W{week:2} {ap_display:4} {coaches_display:8} {playoff_display:4}")
                
            # Calculate ranking trends
            recent_rankings = rankings[:5]  # Last 5 weeks
            if len(recent_rankings) >= 2:
                start_rank = recent_rankings[-1][2]  # AP rank 5 weeks ago
                current_rank = recent_rankings[0][2]  # Current AP rank
                
                if start_rank and current_rank:
                    trend = start_rank - current_rank  # Positive = moving up
                    if trend > 0:
                        print(f"   📈 TRENDING UP: +{trend} spots in last 5 weeks")
                    elif trend < 0:
                        print(f"   📉 TRENDING DOWN: {trend} spots in last 5 weeks")
                    else:
                        print(f"   ➡️  STABLE: No change in last 5 weeks")
        else:
            print(f"   ❌ No team rankings found")
        
        # Also check coach poll rankings
        coach_rankings_query = """
        SELECT season, week, rank
        FROM rankings 
        WHERE school = ?
        ORDER BY season DESC, week DESC
        LIMIT 10
        """
        
        coach_rankings = cursor.execute(coach_rankings_query, [team]).fetchall()
        
        if coach_rankings:
            print(f"\n   👨‍💼 COACH POLL HISTORY (Last 10 weeks):")
            print(f"   {'Season':6} {'Week':4} {'Rank':6}")
            print(f"   {'-'*20}")
            for season, week, rank in coach_rankings:
                print(f"   {season:6} W{week:2} #{rank:2}")
    
    conn.close()

if __name__ == "__main__":
    analyze_cfp_rankings()