#!/usr/bin/env python3
"""
Enhanced CFP Analysis with 2024-2025 Historical Data
Now includes 2024 season for better trend analysis
"""

import sqlite3
from datetime import datetime
import statistics

class Enhanced2YearCFPAnalyzer:
    def __init__(self):
        self.db_path = 'instance/playoff_team_analysis.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # 2025 CFP Teams (confirmed correct)
        self.cfp_teams = [
            'Indiana', 'Ohio State', 'Georgia', 'Texas Tech', 'Oregon', 
            'Ole Miss', 'Texas A&M', 'Oklahoma', 'Alabama', 'Miami', 
            'Tulane', 'James Madison'
        ]
        
        # First Round Matchups
        self.first_round = [
            ('Indiana', 'James Madison'),
            ('Ohio State', 'Oregon'), 
            ('Georgia', 'Alabama'),
            ('Texas Tech', 'Miami'),
            ('Ole Miss', 'Oklahoma'),
            ('Texas A&M', 'Tulane')
        ]
        
    def analyze_2year_trends(self):
        """Analyze 2024 vs 2025 performance trends"""
        print("📈 TWO-YEAR PERFORMANCE TRENDS (2024 → 2025)")
        print("=" * 60)
        
        trends = {}
        
        for team in self.cfp_teams:
            # Get 2024 stats
            self.cursor.execute("""
                SELECT COUNT(*) as games,
                       SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) as wins,
                       AVG(coach_score) as avg_scored,
                       AVG(opponent_score) as avg_allowed
                FROM games WHERE school = ? AND season = 2024
            """, [team])
            
            stats_2024 = self.cursor.fetchone()
            
            # Get 2025 stats  
            self.cursor.execute("""
                SELECT COUNT(*) as games,
                       SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) as wins,
                       AVG(coach_score) as avg_scored,
                       AVG(opponent_score) as avg_allowed
                FROM games WHERE school = ? AND season = 2025
            """, [team])
            
            stats_2025 = self.cursor.fetchone()
            
            if stats_2024[0] > 0 and stats_2025[0] > 0:
                # Calculate trends
                win_pct_2024 = stats_2024[1] / stats_2024[0]
                win_pct_2025 = stats_2025[1] / stats_2025[0]
                
                scoring_trend = stats_2025[2] - stats_2024[2]
                defense_trend = stats_2024[3] - stats_2025[3]  # Lower allowed is better
                
                trends[team] = {
                    '2024_record': f"{stats_2024[1]}-{stats_2024[0] - stats_2024[1]}",
                    '2025_record': f"{stats_2025[1]}-{stats_2025[0] - stats_2025[1]}",
                    'win_pct_change': win_pct_2025 - win_pct_2024,
                    'scoring_trend': scoring_trend,
                    'defense_trend': defense_trend,
                    '2025_margin': stats_2025[2] - stats_2025[3]
                }
                
        # Display trends
        print("Team              2024     2025     Win%Δ   OffΔ   DefΔ   2025Margin")
        print("-" * 70)
        
        for team in sorted(trends.keys()):
            t = trends[team]
            win_change = f"{t['win_pct_change']:+.3f}"
            scoring_change = f"{t['scoring_trend']:+.1f}"
            defense_change = f"{t['defense_trend']:+.1f}"
            margin = f"{t['2025_margin']:.1f}"
            
            print(f"{team:<15} {t['2024_record']:<8} {t['2025_record']:<8} {win_change:<7} {scoring_change:<6} {defense_change:<6} {margin}")
            
        return trends
    
    def find_head_to_head_history(self, team1, team2):
        """Find historical head-to-head between two teams"""
        self.cursor.execute("""
            SELECT season, result, coach_score, opponent_score
            FROM games 
            WHERE school = ? AND opponent = ? AND season >= 2024
            ORDER BY season DESC
        """, [team1, team2])
        
        return self.cursor.fetchall()
    
    def analyze_common_opponents(self, team1, team2):
        """Analyze performance against common opponents"""
        self.cursor.execute("""
            SELECT t1.opponent,
                   t1.coach_score - t1.opponent_score as team1_margin,
                   t2.coach_score - t2.opponent_score as team2_margin,
                   t1.season
            FROM games t1
            JOIN games t2 ON t1.opponent = t2.opponent AND t1.season = t2.season
            WHERE t1.school = ? AND t2.school = ? 
            AND t1.season IN (2024, 2025)
        """, [team1, team2])
        
        return self.cursor.fetchall()
    
    def predict_first_round_matchups(self):
        """Predict first round CFP matchups with enhanced data"""
        print("\n🏈 FIRST ROUND CFP PREDICTIONS (2024-2025 Data)")
        print("=" * 60)
        
        for team1, team2 in self.first_round:
            print(f"\n⚔️  {team1} vs {team2}")
            print("-" * 30)
            
            # Head-to-head history
            h2h = self.find_head_to_head_history(team1, team2)
            if h2h:
                print("   📚 Recent head-to-head:")
                for season, result, scored, allowed in h2h:
                    print(f"      {season}: {result} {scored}-{allowed}")
            else:
                print("   📚 No recent head-to-head")
            
            # Common opponents
            common = self.analyze_common_opponents(team1, team2)
            if common:
                margins1 = [margin1 for _, margin1, _, _ in common]
                margins2 = [margin2 for _, _, margin2, _ in common]
                
                avg_margin1 = statistics.mean(margins1)
                avg_margin2 = statistics.mean(margins2)
                advantage = avg_margin1 - avg_margin2
                
                print(f"   🎯 Common opponents ({len(common)}):")
                print(f"      {team1} avg margin: {avg_margin1:+.1f}")
                print(f"      {team2} avg margin: {avg_margin2:+.1f}")
                print(f"      → {team1 if advantage > 0 else team2} advantage: {abs(advantage):.1f} pts")
            
            # 2025 stats comparison
            stats = {}
            for team in [team1, team2]:
                self.cursor.execute("""
                    SELECT AVG(coach_score) as scored, AVG(opponent_score) as allowed
                    FROM games WHERE school = ? AND season = 2025
                """, [team])
                
                scored, allowed = self.cursor.fetchone()
                stats[team] = {'scored': scored, 'allowed': allowed, 'margin': scored - allowed}
            
            # Prediction
            if stats[team1]['margin'] > stats[team2]['margin']:
                favorite = team1
                margin_diff = stats[team1]['margin'] - stats[team2]['margin']
            else:
                favorite = team2
                margin_diff = stats[team2]['margin'] - stats[team1]['margin']
                
            print(f"   📊 2025 Scoring Margins:")
            print(f"      {team1}: {stats[team1]['margin']:+.1f} ({stats[team1]['scored']:.1f} - {stats[team1]['allowed']:.1f})")
            print(f"      {team2}: {stats[team2]['margin']:+.1f} ({stats[team2]['scored']:.1f} - {stats[team2]['allowed']:.1f})")
            print(f"   🎯 PREDICTION: {favorite} by {margin_diff:.1f}")
    
    def identify_tournament_sleepers(self, trends):
        """Identify potential tournament sleepers based on trends"""
        print("\n🌟 TOURNAMENT SLEEPERS & RISERS")
        print("=" * 40)
        
        # Teams with biggest improvement
        improvers = [(team, data['win_pct_change']) for team, data in trends.items() 
                    if data['win_pct_change'] > 0.1]
        improvers.sort(key=lambda x: x[1], reverse=True)
        
        print("Biggest improvers from 2024:")
        for team, improvement in improvers[:3]:
            print(f"   🔥 {team}: {improvement:+.3f} win% improvement")
            
        # Teams with best 2025 margins
        margins = [(team, data['2025_margin']) for team, data in trends.items()]
        margins.sort(key=lambda x: x[1], reverse=True)
        
        print("\nBest 2025 point differentials:")
        for team, margin in margins[:3]:
            print(f"   ⚡ {team}: {margin:+.1f} point margin")
    
    def run_enhanced_analysis(self):
        """Run complete enhanced analysis"""
        print("🏆 ENHANCED CFP ANALYSIS (2024-2025)")
        print("=" * 70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Data: 2024 & 2025 seasons for trend analysis")
        
        trends = self.analyze_2year_trends()
        self.predict_first_round_matchups()
        self.identify_tournament_sleepers(trends)
        
        print("\n" + "=" * 70)
        print("✅ ENHANCED ANALYSIS COMPLETE")
        print("🎯 Predictions based on 2-year performance data")
        print("📈 Trend analysis shows team trajectory")
        
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    analyzer = Enhanced2YearCFPAnalyzer()
    try:
        analyzer.run_enhanced_analysis()
    finally:
        analyzer.close()