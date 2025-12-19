#!/usr/bin/env python3
"""
Comprehensive Data Fact Checker
Validates all remaining data for accuracy and realism
"""

import sqlite3
from collections import defaultdict, Counter
import statistics

class ComprehensiveFactChecker:
    def __init__(self):
        self.db_path = 'instance/playoff_team_analysis.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Known CFP teams that should be in playoff
        self.known_cfp_2025 = {
            'Oregon', 'Georgia', 'Boise State', 'Arizona State', 
            'Texas', 'Penn State', 'Notre Dame', 'Ohio State',
            'Indiana', 'Tennessee', 'SMU', 'Clemson'
        }
        
        # Teams that definitely should NOT be CFP teams in 2025
        self.impossible_cfp = {
            'James Madison', 'Tulane', 'Texas Tech', 'Miami', 
            'Ole Miss', 'Texas A&M', 'Oklahoma', 'Alabama'
        }
        
    def check_impossible_records(self):
        """Check for impossible win-loss records"""
        print("🔍 CHECKING FOR IMPOSSIBLE RECORDS")
        print("=" * 40)
        
        issues = []
        
        # Check for perfect seasons that seem impossible
        self.cursor.execute("""
            SELECT school, season, 
                   COUNT(*) as games,
                   SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) as wins,
                   SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) as losses
            FROM games 
            WHERE season = 2025
            GROUP BY school, season
            HAVING wins > 15 OR (wins = games AND games > 13)
        """)
        
        perfect_seasons = self.cursor.fetchall()
        for school, season, games, wins, losses in perfect_seasons:
            if games > 15:  # Impossible - max is ~15 games
                issues.append(f"❌ {school}: {wins}-{losses} ({games} games) - Too many games")
            elif wins == games and games > 13:
                issues.append(f"⚠️  {school}: Perfect {wins}-0 - Verify if realistic")
                
        if not issues:
            print("✅ No impossible records found")
        else:
            for issue in issues:
                print(f"   {issue}")
                
        return issues
    
    def check_impossible_scores(self):
        """Check for impossible game scores"""
        print("\n🔍 CHECKING FOR IMPOSSIBLE SCORES")
        print("=" * 40)
        
        issues = []
        
        # Check for extremely high scores
        self.cursor.execute("""
            SELECT school, opponent, season, week, coach_score, opponent_score
            FROM games 
            WHERE coach_score > 100 OR opponent_score > 100
        """)
        
        high_scores = self.cursor.fetchall()
        for game in high_scores:
            issues.append(f"❌ Impossible high score: {game[0]} vs {game[1]} - {game[4]}-{game[5]}")
            
        # Check for negative scores
        self.cursor.execute("""
            SELECT school, opponent, season, week, coach_score, opponent_score
            FROM games 
            WHERE coach_score < 0 OR opponent_score < 0
        """)
        
        negative_scores = self.cursor.fetchall()
        for game in negative_scores:
            issues.append(f"❌ Negative score: {game[0]} vs {game[1]} - {game[4]}-{game[5]}")
            
        # Check for ties in football (very rare)
        self.cursor.execute("""
            SELECT school, opponent, season, week, coach_score, opponent_score
            FROM games 
            WHERE coach_score = opponent_score AND season > 2000
        """)
        
        ties = self.cursor.fetchall()
        for game in ties:
            issues.append(f"⚠️  Tie game (rare): {game[0]} vs {game[1]} - {game[4]}-{game[5]}")
            
        if not issues:
            print("✅ No impossible scores found")
        else:
            for issue in issues:
                print(f"   {issue}")
                
        return issues
    
    def check_cfp_team_validity(self):
        """Check if CFP teams in database are actually correct"""
        print("\n🏆 CHECKING CFP TEAM VALIDITY")
        print("=" * 40)
        
        # Get teams marked as CFP in our analysis
        cfp_in_db = {'Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 
                    'Ole Miss', 'Texas A&M', 'Oklahoma', 'Alabama', 'Miami', 
                    'Tulane', 'James Madison'}
        
        print("Teams in our CFP analysis:")
        for team in sorted(cfp_in_db):
            if team in self.impossible_cfp:
                print(f"   ❌ {team} - NOT in actual 2025 CFP")
            elif team in self.known_cfp_2025:
                print(f"   ✅ {team} - Correctly in CFP")
            else:
                print(f"   ⚠️  {team} - Need to verify")
                
        # Missing actual CFP teams
        missing = self.known_cfp_2025 - cfp_in_db
        if missing:
            print("\nMissing actual CFP teams:")
            for team in sorted(missing):
                print(f"   ❌ {team} - Should be in CFP but not in our analysis")
                
        return cfp_in_db, missing
    
    def check_team_name_consistency(self):
        """Check for inconsistent team naming"""
        print("\n📝 CHECKING TEAM NAME CONSISTENCY")
        print("=" * 40)
        
        # Get all unique team names
        self.cursor.execute("SELECT DISTINCT school FROM games ORDER BY school")
        teams = [row[0] for row in self.cursor.fetchall()]
        
        # Look for potential name variations
        name_issues = []
        team_variations = {}
        
        for team in teams:
            # Check for common variations
            if 'State' in team:
                base_name = team.replace(' State', '')
                variations = [t for t in teams if base_name in t and t != team]
                if variations:
                    team_variations[team] = variations
                    
        # Check for suspicious team names
        suspicious = []
        for team in teams:
            if len(team) < 3:  # Too short
                suspicious.append(f"❌ '{team}' - Name too short")
            elif team.count(' ') > 3:  # Too many spaces
                suspicious.append(f"⚠️  '{team}' - Complex name, verify accuracy")
                
        if team_variations:
            print("Potential name variations found:")
            for main, variations in team_variations.items():
                print(f"   ⚠️  {main} has variations: {variations}")
                
        if suspicious:
            print("Suspicious team names:")
            for issue in suspicious:
                print(f"   {issue}")
                
        if not team_variations and not suspicious:
            print("✅ Team names appear consistent")
            
        return team_variations, suspicious
    
    def check_scoring_realism(self):
        """Check if scoring patterns are realistic"""
        print("\n🏈 CHECKING SCORING REALISM")
        print("=" * 40)
        
        issues = []
        
        # Check average scoring per team
        self.cursor.execute("""
            SELECT school, 
                   AVG(coach_score) as avg_scored,
                   AVG(opponent_score) as avg_allowed,
                   MAX(coach_score) as max_scored,
                   MIN(coach_score) as min_scored
            FROM games 
            WHERE season = 2025
            GROUP BY school
            HAVING COUNT(*) >= 5
        """)
        
        team_scoring = self.cursor.fetchall()
        
        for school, avg_scored, avg_allowed, max_scored, min_scored in team_scoring:
            # Check for unrealistic averages
            if avg_scored > 60:
                issues.append(f"❌ {school}: Avg {avg_scored:.1f} PPG - Too high")
            elif avg_scored < 5:
                issues.append(f"❌ {school}: Avg {avg_scored:.1f} PPG - Too low")
                
            if max_scored > 80:
                issues.append(f"⚠️  {school}: High game {max_scored} pts - Verify")
                
            if min_scored == 0 and avg_scored > 20:  # Shutout but normally scores well
                issues.append(f"⚠️  {school}: Shutout game but avg {avg_scored:.1f} PPG")
        
        # Check for teams that never lose
        self.cursor.execute("""
            SELECT school, COUNT(*) as games,
                   SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) as losses
            FROM games 
            WHERE season = 2025
            GROUP BY school
            HAVING COUNT(*) >= 10 AND losses = 0
        """)
        
        undefeated = self.cursor.fetchall()
        for school, games, losses in undefeated:
            if games >= 12:  # Perfect season with 12+ games is very rare
                issues.append(f"⚠️  {school}: Perfect {games}-0 season - Verify accuracy")
        
        if not issues:
            print("✅ Scoring patterns appear realistic")
        else:
            for issue in issues:
                print(f"   {issue}")
                
        return issues
    
    def check_conference_logic(self):
        """Check if matchups make conference sense"""
        print("\n🏟️ CHECKING CONFERENCE MATCHUP LOGIC")
        print("=" * 40)
        
        # Look for teams that play each other too frequently (non-conference rivals)
        self.cursor.execute("""
            SELECT school, opponent, COUNT(*) as games
            FROM games 
            WHERE season >= 2020
            GROUP BY school, opponent
            HAVING COUNT(*) > 8 AND school < opponent  -- Avoid duplicates
            ORDER BY games DESC
        """)
        
        frequent_matchups = self.cursor.fetchall()
        
        issues = []
        for school, opponent, games in frequent_matchups:
            # These should probably be conference rivals
            if games > 10:
                issues.append(f"⚠️  {school} vs {opponent}: {games} games since 2020 - Conference rivals?")
        
        # Check for impossible conference matchups
        known_conferences = {
            'SEC': ['Alabama', 'Georgia', 'Ole Miss', 'Texas A&M', 'Oklahoma'],
            'Big Ten': ['Ohio State', 'Indiana', 'Oregon'],
            'Big 12': ['Texas Tech'],
            'ACC': ['Miami'],
            'AAC': ['Tulane'],
            'Sun Belt': ['James Madison']
        }
        
        for conf_name, conf_teams in known_conferences.items():
            for i, team1 in enumerate(conf_teams):
                for team2 in conf_teams[i+1:]:
                    # Check if conference teams play each other appropriately
                    self.cursor.execute("""
                        SELECT COUNT(*) FROM games 
                        WHERE school = ? AND opponent = ? AND season = 2025
                    """, [team1, team2])
                    
                    games = self.cursor.fetchone()[0]
                    if games == 0:
                        issues.append(f"⚠️  {team1} vs {team2}: No 2025 game ({conf_name} teams)")
        
        if not issues:
            print("✅ Conference matchups appear logical")
        else:
            print("Conference logic issues:")
            for issue in issues:
                print(f"   {issue}")
                
        return issues
    
    def generate_fact_check_report(self):
        """Generate comprehensive fact-check report"""
        print("\n📋 COMPREHENSIVE FACT CHECK REPORT")
        print("=" * 50)
        
        all_issues = []
        
        # Run all checks
        record_issues = self.check_impossible_records()
        score_issues = self.check_impossible_scores()
        cfp_issues = self.check_cfp_team_validity()
        name_issues = self.check_team_name_consistency()
        scoring_issues = self.check_scoring_realism()
        conference_issues = self.check_conference_logic()
        
        all_issues.extend(record_issues)
        all_issues.extend(score_issues)
        all_issues.extend(scoring_issues)
        all_issues.extend(conference_issues)
        
        print(f"\n📊 FACT CHECK SUMMARY:")
        print(f"   Total issues found: {len(all_issues)}")
        
        if len(all_issues) == 0:
            print("   ✅ ALL DATA APPEARS ACCURATE!")
        else:
            print("   ⚠️  Issues need review:")
            for issue in all_issues[:10]:  # Show first 10
                print(f"      {issue}")
            if len(all_issues) > 10:
                print(f"      ... and {len(all_issues) - 10} more issues")
        
        return all_issues
    
    def run_comprehensive_fact_check(self):
        """Run complete fact checking process"""
        print("🔍 COMPREHENSIVE FACT CHECK")
        print("=" * 60)
        print("Verifying all data for accuracy and realism...")
        
        issues = self.generate_fact_check_report()
        
        print("\n" + "=" * 60)
        if len(issues) == 0:
            print("✅ FACT CHECK PASSED - DATA IS ACCURATE")
        else:
            print("⚠️  FACT CHECK FOUND ISSUES - REVIEW NEEDED")
            
        print("🎯 Fact checking complete")
        
        return issues
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    checker = ComprehensiveFactChecker()
    try:
        checker.run_comprehensive_fact_check()
    finally:
        checker.close()