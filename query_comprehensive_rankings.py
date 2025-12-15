#!/usr/bin/env python3
"""
Query Comprehensive Power Rankings from Database
"""

import json
import sqlite3
import argparse

DB_PATH = 'instance/predictions.db'

def get_team_rankings(team_name, season=2025, week=15):
    """Get comprehensive rankings for a specific team"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            team_name, conference, rank, 
            overall_score, offensive_score, defensive_score,
            total_metrics_analyzed,
            offensive_normalized_json, defensive_normalized_json,
            offensive_raw_json, defensive_raw_json,
            generated_at
        FROM comprehensive_power_rankings
        WHERE team_name = ? AND season = ? AND week = ?
    """, (team_name, season, week))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        'team_name': row[0],
        'conference': row[1],
        'rank': row[2],
        'overall_score': row[3],
        'offensive_score': row[4],
        'defensive_score': row[5],
        'total_metrics_analyzed': row[6],
        'offensive_normalized': json.loads(row[7]),
        'defensive_normalized': json.loads(row[8]),
        'offensive_raw': json.loads(row[9]),
        'defensive_raw': json.loads(row[10]),
        'generated_at': row[11]
    }

def get_top_teams(limit=10, season=2025, week=15):
    """Get top N teams by overall score"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            rank, team_name, conference, 
            overall_score, offensive_score, defensive_score
        FROM comprehensive_power_rankings
        WHERE season = ? AND week = ?
        ORDER BY rank
        LIMIT ?
    """, (season, week, limit))
    
    teams = cursor.fetchall()
    conn.close()
    
    return [
        {
            'rank': row[0],
            'team': row[1],
            'conference': row[2],
            'overall_score': row[3],
            'offensive_score': row[4],
            'defensive_score': row[5]
        }
        for row in teams
    ]

def get_conference_rankings(conference, season=2025, week=15):
    """Get all teams in a specific conference"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            rank, team_name, overall_score, 
            offensive_score, defensive_score
        FROM comprehensive_power_rankings
        WHERE conference = ? AND season = ? AND week = ?
        ORDER BY rank
    """, (conference, season, week))
    
    teams = cursor.fetchall()
    conn.close()
    
    return [
        {
            'rank': row[0],
            'team': row[1],
            'overall_score': row[2],
            'offensive_score': row[3],
            'defensive_score': row[4]
        }
        for row in teams
    ]

def main():
    parser = argparse.ArgumentParser(description='Query comprehensive power rankings')
    parser.add_argument('--team', help='Team name to query')
    parser.add_argument('--top', type=int, default=10, help='Show top N teams')
    parser.add_argument('--conference', help='Show teams in conference')
    parser.add_argument('--season', type=int, default=2025, help='Season')
    parser.add_argument('--week', type=int, default=15, help='Week')
    
    args = parser.parse_args()
    
    if args.team:
        data = get_team_rankings(args.team, args.season, args.week)
        if data:
            print(f"\n{'='*60}")
            print(f"#{data['rank']} {data['team_name']} ({data['conference']})")
            print(f"{'='*60}")
            print(f"Overall Score: {data['overall_score']:.2f}")
            print(f"Offensive Score: {data['offensive_score']:.2f}")
            print(f"Defensive Score: {data['defensive_score']:.2f}")
            print(f"Total Metrics: {data['total_metrics_analyzed']}")
            
            print(f"\nTop Offensive Metrics (Normalized):")
            off_norm = data['offensive_normalized']
            sorted_off = sorted(off_norm.items(), key=lambda x: x[1] if x[1] is not None else 0, reverse=True)[:5]
            for metric, value in sorted_off:
                print(f"  {metric}: {value:.2f}")
            
            print(f"\nTop Defensive Metrics (Normalized):")
            def_norm = data['defensive_normalized']
            sorted_def = sorted(def_norm.items(), key=lambda x: x[1] if x[1] is not None else 0, reverse=True)[:5]
            for metric, value in sorted_def:
                print(f"  {metric}: {value:.2f}")
        else:
            print(f"Team '{args.team}' not found")
    
    elif args.conference:
        teams = get_conference_rankings(args.conference, args.season, args.week)
        print(f"\n{args.conference} Rankings")
        print(f"{'='*60}")
        for team in teams:
            print(f"#{team['rank']:3d} {team['team']:30s} Overall: {team['overall_score']:5.2f}")
    
    else:
        teams = get_top_teams(args.top, args.season, args.week)
        print(f"\nTop {args.top} Teams - Season {args.season}, Week {args.week}")
        print(f"{'='*80}")
        print(f"{'Rank':<5} {'Team':<25} {'Conference':<15} {'Overall':<8} {'Off':<8} {'Def':<8}")
        print(f"{'-'*80}")
        for team in teams:
            print(f"{team['rank']:<5} {team['team']:<25} {team['conference']:<15} "
                  f"{team['overall_score']:<8.2f} {team['offensive_score']:<8.2f} {team['defensive_score']:<8.2f}")

if __name__ == '__main__':
    main()
