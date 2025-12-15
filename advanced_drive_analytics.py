"""
Advanced Drive Analytics Module
Provides deep drive efficiency metrics and quarter-by-quarter predictions
"""

import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class AdvancedDriveAnalytics:
    """Calculate advanced drive metrics from drives_complete table"""
    
    def __init__(self, db_path: str = 'instance/predictions.db'):
        self.db_path = db_path
    
    def get_team_drive_metrics(self, team_name: str, season: int = 2025) -> Dict:
        """Get comprehensive drive metrics for a team"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Query all drive metrics
        query = """
        SELECT 
            COUNT(*) as total_drives,
            AVG(CAST(yards AS FLOAT)) as avg_yards_per_drive,
            AVG(CAST(plays_count AS FLOAT)) as avg_plays_per_drive,
            AVG(CAST(elapsed_minutes AS FLOAT) + CAST(elapsed_seconds AS FLOAT)/60.0) as avg_time_minutes,
            
            -- Scoring metrics
            SUM(CASE WHEN scoring = 1 THEN 1 ELSE 0 END) as scoring_drives,
            SUM(CASE WHEN drive_result = 'TD' OR drive_result LIKE '%TD' THEN 1 ELSE 0 END) as td_drives,
            SUM(CASE WHEN drive_result = 'FG' THEN 1 ELSE 0 END) as fg_drives,
            
            -- Negative outcomes
            SUM(CASE WHEN drive_result = 'PUNT' THEN 1 ELSE 0 END) as punts,
            SUM(CASE WHEN drive_result IN ('INT', 'FUMBLE') THEN 1 ELSE 0 END) as turnovers,
            SUM(CASE WHEN drive_result = 'DOWNS' THEN 1 ELSE 0 END) as turnover_on_downs,
            SUM(CASE WHEN plays_count = 3 AND drive_result = 'PUNT' THEN 1 ELSE 0 END) as three_and_outs,
            
            -- Advanced efficiency
            SUM(CASE WHEN start_yards_to_goal <= 20 THEN 1 ELSE 0 END) as red_zone_attempts,
            SUM(CASE WHEN start_yards_to_goal <= 20 AND scoring = 1 THEN 1 ELSE 0 END) as red_zone_scores,
            SUM(CASE WHEN yards >= 75 THEN 1 ELSE 0 END) as explosive_drives,
            SUM(CASE WHEN plays_count <= 3 AND scoring = 1 THEN 1 ELSE 0 END) as quick_strikes,
            SUM(CASE WHEN plays_count >= 10 THEN 1 ELSE 0 END) as methodical_drives,
            SUM(CASE WHEN elapsed_minutes >= 5 THEN 1 ELSE 0 END) as clock_killers,
            
            -- Field position
            SUM(CASE WHEN start_yards_to_goal <= 50 THEN 1 ELSE 0 END) as short_field_drives,
            SUM(CASE WHEN start_yards_to_goal <= 50 AND scoring = 1 THEN 1 ELSE 0 END) as short_field_scores,
            SUM(CASE WHEN start_yards_to_goal >= 80 THEN 1 ELSE 0 END) as long_field_drives,
            SUM(CASE WHEN start_yards_to_goal >= 80 AND scoring = 1 THEN 1 ELSE 0 END) as long_field_scores,
            
            -- Opening drive
            SUM(CASE WHEN drive_number = 1 AND scoring = 1 THEN 1 ELSE 0 END) as opening_drive_scores,
            
            -- Comeback drives
            SUM(CASE WHEN start_defense_score > start_offense_score AND scoring = 1 THEN 1 ELSE 0 END) as comeback_scoring_drives
            
        FROM drives_complete 
        WHERE offense = ? AND season = ?
        """
        
        cursor.execute(query, (team_name, season))
        row = cursor.fetchone()
        
        if not row or row[0] == 0:
            conn.close()
            return self._empty_metrics()
        
        # Calculate percentages
        total_drives = row[0]
        metrics = {
            'total_drives': total_drives,
            'avg_yards_per_drive': round(row[1] or 0, 2),
            'avg_plays_per_drive': round(row[2] or 0, 2),
            'avg_time_per_drive': round(row[3] or 0, 2),
            
            'scoring_drives': row[4],
            'scoring_pct': round((row[4] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'td_drives': row[5],
            'td_pct': round((row[5] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'fg_drives': row[6],
            'fg_pct': round((row[6] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'punts': row[7],
            'punt_pct': round((row[7] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'turnovers': row[8],
            'turnover_pct': round((row[8] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'turnover_on_downs': row[9],
            'three_and_outs': row[10],
            'three_and_out_pct': round((row[10] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'red_zone_attempts': row[11],
            'red_zone_scores': row[12],
            'red_zone_efficiency': round((row[12] / row[11] * 100) if row[11] > 0 else 0, 1),
            
            'explosive_drives': row[13],
            'explosive_pct': round((row[13] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'quick_strikes': row[14],
            'quick_strike_pct': round((row[14] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'methodical_drives': row[15],
            'methodical_pct': round((row[15] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'clock_killers': row[16],
            'clock_killer_pct': round((row[16] / total_drives * 100) if total_drives > 0 else 0, 1),
            
            'short_field_drives': row[17],
            'short_field_scores': row[18],
            'short_field_pct': round((row[18] / row[17] * 100) if row[17] > 0 else 0, 1),
            
            'long_field_drives': row[19],
            'long_field_scores': row[20],
            'long_field_pct': round((row[20] / row[19] * 100) if row[19] > 0 else 0, 1),
            
            'opening_drive_scores': row[21],
            'comeback_drives': row[22]
        }
        
        # Get quarter breakdown
        metrics['quarter_performance'] = self._get_quarter_breakdown(cursor, team_name, season)
        
        conn.close()
        return metrics
    
    def _get_quarter_breakdown(self, cursor, team_name: str, season: int) -> Dict:
        """Get scoring efficiency by quarter"""
        
        query = """
        SELECT 
            start_period as quarter,
            COUNT(*) as drives,
            SUM(CASE WHEN scoring = 1 THEN 1 ELSE 0 END) as scoring,
            AVG(CAST(yards AS FLOAT)) as avg_yards
        FROM drives_complete 
        WHERE offense = ? AND season = ? AND start_period IS NOT NULL
        GROUP BY start_period
        ORDER BY start_period
        """
        
        cursor.execute(query, (team_name, season))
        rows = cursor.fetchall()
        
        quarters = {}
        for row in rows:
            quarter = row[0]
            total = row[1]
            scoring = row[2]
            quarters[f'Q{quarter}'] = {
                'drives': total,
                'scoring': scoring,
                'scoring_pct': round((scoring / total * 100) if total > 0 else 0, 1),
                'avg_yards': round(row[3] or 0, 1)
            }
        
        return quarters
    
    def _empty_metrics(self) -> Dict:
        """Return empty metrics structure"""
        return {
            'total_drives': 0,
            'avg_yards_per_drive': 0,
            'avg_plays_per_drive': 0,
            'avg_time_per_drive': 0,
            'scoring_pct': 0,
            'td_pct': 0,
            'fg_pct': 0,
            'punt_pct': 0,
            'turnover_pct': 0,
            'three_and_out_pct': 0,
            'red_zone_efficiency': 0,
            'explosive_pct': 0,
            'quick_strike_pct': 0,
            'methodical_pct': 0,
            'clock_killer_pct': 0,
            'short_field_pct': 0,
            'long_field_pct': 0,
            'quarter_performance': {}
        }
    
    def predict_quarter_outcomes(self, home_team: str, away_team: str, season: int = 2025) -> Dict:
        """Predict quarter-by-quarter performance based on historical data"""
        
        home_metrics = self.get_team_drive_metrics(home_team, season)
        away_metrics = self.get_team_drive_metrics(away_team, season)
        
        predictions = {}
        
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            home_q = home_metrics['quarter_performance'].get(quarter, {'scoring_pct': 0, 'avg_yards': 0})
            away_q = away_metrics['quarter_performance'].get(quarter, {'scoring_pct': 0, 'avg_yards': 0})
            
            home_score_pct = home_q['scoring_pct']
            away_score_pct = away_q['scoring_pct']
            
            # Determine winner of quarter
            diff = abs(home_score_pct - away_score_pct)
            
            if diff < 5:
                edge = "Even"
                confidence = "Low"
            elif diff < 15:
                edge = home_team if home_score_pct > away_score_pct else away_team
                confidence = "Moderate"
            else:
                edge = home_team if home_score_pct > away_score_pct else away_team
                confidence = "High"
            
            predictions[quarter] = {
                'home_scoring_pct': home_score_pct,
                'away_scoring_pct': away_score_pct,
                'home_avg_yards': home_q.get('avg_yards', 0),
                'away_avg_yards': away_q.get('avg_yards', 0),
                'edge': edge,
                'confidence': confidence,
                'analysis': self._generate_quarter_analysis(quarter, home_team, away_team, home_q, away_q, edge)
            }
        
        return predictions
    
    def _generate_quarter_analysis(self, quarter: str, home_team: str, away_team: str, 
                                   home_q: Dict, away_q: Dict, edge: str) -> str:
        """Generate narrative analysis for quarter"""
        
        quarter_contexts = {
            'Q1': "opening frame establishing tempo",
            'Q2': "second quarter with momentum building",
            'Q3': "critical post-halftime adjustments",
            'Q4': "closing stretch with game on the line"
        }
        
        context = quarter_contexts.get(quarter, quarter)
        
        if edge == "Even":
            return f"{context.capitalize()}: Dead heat expected with both teams averaging similar scoring rates. Execution and field position will be decisive."
        
        winner = edge
        loser = home_team if edge == away_team else away_team
        winner_pct = home_q['scoring_pct'] if edge == home_team else away_q['scoring_pct']
        
        return f"{context.capitalize()}: {winner} holds edge with {winner_pct}% scoring efficiency vs {loser}'s weaker {quarter} performance. Expect {winner} to control pace."


# Singleton instance
drive_analytics = AdvancedDriveAnalytics()
