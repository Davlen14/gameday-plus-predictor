#!/usr/bin/env python3
"""
Generate Comprehensive QB Analysis for Week 14
==============================================
Creates comprehensive QB statistics and rankings for 2025 season
"""

import requests
import json
from datetime import datetime
from typing import Dict, List

class ComprehensiveQBAnalyzer:
    def __init__(self, api_key: str, year: int = 2025):
        self.api_key = api_key
        self.graphql_url = "https://graphql.collegefootballdata.com/v1/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.year = year
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def execute_query(self, query: str, variables: Dict = None) -> Dict:
        """Execute GraphQL query"""
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "errors" in result:
                    print(f"❌ GraphQL Errors: {result['errors']}")
                    return None
                return result.get('data', {})
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return None
    
    def fetch_all_qb_stats(self) -> List[Dict]:
        """Fetch comprehensive QB statistics using REST API"""
        print("🏈 Fetching comprehensive QB statistics...")
        
        # Use REST API instead of GraphQL for player stats
        rest_url = "https://api.collegefootballdata.com/stats/player/season"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                rest_url,
                headers=headers,
                params={"year": self.year, "category": "passing"},
                timeout=30
            )
            
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ Fetched {len(stats)} QB passing records")
                return stats
            else:
                print(f"❌ HTTP Error {response.status_code}")
                return []
        
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return []
    
    def process_qb_stats(self, raw_stats: List[Dict]) -> Dict:
        """Process and aggregate QB statistics by player"""
        print("📊 Processing QB statistics...")
        
        qb_data = {}
        
        for stat in raw_stats:
            player_id = stat.get("playerId")
            if not player_id:
                continue
            
            if player_id not in qb_data:
                qb_data[player_id] = {
                    "player_id": player_id,
                    "name": stat.get("playerName"),
                    "team": stat.get("team"),
                    "team_id": stat.get("teamId"),
                    "conference": stat.get("conference"),
                    "season": self.year,
                    "passing": {},
                    "rushing": {}
                }
            
            stat_type = stat.get("statType", "").lower()
            category = stat.get("category", "").lower()
            value = stat.get("stat", 0)
            
            if stat_type == "passing":
                qb_data[player_id]["passing"][category] = value
            elif stat_type == "rushing":
                qb_data[player_id]["rushing"][category] = value
        
        print(f"✅ Processed stats for {len(qb_data)} quarterbacks")
        return qb_data
    
    def calculate_qb_metrics(self, qb_data: Dict) -> List[Dict]:
        """Calculate comprehensive QB metrics and rankings"""
        print("⚙️  Calculating QB metrics and rankings...")
        
        qb_list = []
        
        for player_id, data in qb_data.items():
            passing = data.get("passing", {})
            rushing = data.get("rushing", {})
            
            # Calculate key metrics
            attempts = passing.get("attempts", 0) or passing.get("pass_att", 0) or 0
            completions = passing.get("completions", 0) or passing.get("pass_cmp", 0) or 0
            yards = passing.get("yards", 0) or passing.get("pass_yds", 0) or 0
            touchdowns = passing.get("touchdowns", 0) or passing.get("pass_td", 0) or 0
            interceptions = passing.get("interceptions", 0) or passing.get("int", 0) or 0
            
            # Skip QBs with very few attempts (likely not starters)
            if attempts < 50:
                continue
            
            # Calculate derived stats
            completion_pct = (completions / attempts * 100) if attempts > 0 else 0
            yards_per_attempt = (yards / attempts) if attempts > 0 else 0
            td_int_ratio = (touchdowns / interceptions) if interceptions > 0 else touchdowns
            
            # Rushing stats for dual-threat rating
            rush_att = rushing.get("attempts", 0) or rushing.get("rush_att", 0) or 0
            rush_yds = rushing.get("yards", 0) or rushing.get("rush_yds", 0) or 0
            rush_td = rushing.get("touchdowns", 0) or rushing.get("rush_td", 0) or 0
            
            # Calculate passer rating (simplified NCAA formula)
            passer_rating = 0
            if attempts > 0:
                comp_component = (completion_pct - 30) * 0.05
                yds_component = (yards_per_attempt - 3) * 0.25
                td_component = (touchdowns / attempts * 100) * 0.2
                int_component = (interceptions / attempts * 100) * 0.25
                passer_rating = ((comp_component + yds_component + td_component - int_component) * 100) / 3
            
            qb_metrics = {
                "player_id": player_id,
                "name": data.get("name"),
                "team": data.get("team"),
                "conference": data.get("conference"),
                "season": self.year,
                "passing_stats": {
                    "attempts": attempts,
                    "completions": completions,
                    "yards": yards,
                    "touchdowns": touchdowns,
                    "interceptions": interceptions,
                    "completion_percentage": round(completion_pct, 1),
                    "yards_per_attempt": round(yards_per_attempt, 2),
                    "td_int_ratio": round(td_int_ratio, 2),
                    "passer_rating": round(passer_rating, 1)
                },
                "rushing_stats": {
                    "attempts": rush_att,
                    "yards": rush_yds,
                    "touchdowns": rush_td,
                    "yards_per_carry": round(rush_yds / rush_att, 2) if rush_att > 0 else 0
                },
                "total_stats": {
                    "total_yards": yards + rush_yds,
                    "total_touchdowns": touchdowns + rush_td,
                    "total_plays": attempts + rush_att
                }
            }
            
            qb_list.append(qb_metrics)
        
        print(f"✅ Calculated metrics for {len(qb_list)} qualified QBs")
        return qb_list
    
    def generate_rankings(self, qb_list: List[Dict]):
        """Generate all QB ranking files"""
        print("\n📊 Generating QB ranking files...")
        
        # 1. Passer Rating Rankings
        passer_rating_rankings = sorted(
            [qb for qb in qb_list if qb["passing_stats"]["attempts"] >= 100],
            key=lambda x: x["passing_stats"]["passer_rating"],
            reverse=True
        )
        
        self.save_ranking_file(
            passer_rating_rankings,
            "qb_passer_rating_rankings",
            "Passer Rating",
            "passer_rating"
        )
        
        # 2. Total Yards Rankings
        total_yards_rankings = sorted(
            qb_list,
            key=lambda x: x["total_stats"]["total_yards"],
            reverse=True
        )
        
        self.save_ranking_file(
            total_yards_rankings,
            "qb_total_yards_rankings",
            "Total Yards",
            "total_yards"
        )
        
        # 3. Ball Security Score (TD:INT ratio + low fumbles)
        ball_security_rankings = sorted(
            [qb for qb in qb_list if qb["passing_stats"]["interceptions"] > 0],
            key=lambda x: x["passing_stats"]["td_int_ratio"],
            reverse=True
        )
        
        self.save_ranking_file(
            ball_security_rankings,
            "qb_ball_security_score_rankings",
            "Ball Security (TD:INT Ratio)",
            "ball_security"
        )
        
        # 4. Dual-Threat Efficiency (for QBs with significant rushing)
        dual_threat_rankings = sorted(
            [qb for qb in qb_list if qb["rushing_stats"]["attempts"] >= 30],
            key=lambda x: x["total_stats"]["total_yards"] / x["total_stats"]["total_plays"],
            reverse=True
        )
        
        self.save_ranking_file(
            dual_threat_rankings,
            "qb_dual_threat_efficiency_rankings",
            "Dual-Threat Efficiency",
            "dual_threat"
        )
        
        # 5. Comprehensive Efficiency Score
        # Composite: 40% rating + 30% TD:INT + 20% YPA + 10% completion%
        for qb in qb_list:
            ps = qb["passing_stats"]
            rating_score = min(ps["passer_rating"] / 2, 100)  # Normalize to 100
            td_int_score = min(ps["td_int_ratio"] * 10, 100)  # Normalize to 100
            ypa_score = min(ps["yards_per_attempt"] * 10, 100)  # Normalize to 100
            comp_score = ps["completion_percentage"]
            
            qb["comprehensive_efficiency"] = round(
                (rating_score * 0.4) + (td_int_score * 0.3) + (ypa_score * 0.2) + (comp_score * 0.1),
                2
            )
        
        comprehensive_rankings = sorted(
            [qb for qb in qb_list if qb["passing_stats"]["attempts"] >= 100],
            key=lambda x: x.get("comprehensive_efficiency", 0),
            reverse=True
        )
        
        self.save_ranking_file(
            comprehensive_rankings,
            "qb_comprehensive_efficiency_score_rankings",
            "Comprehensive Efficiency Score",
            "comprehensive"
        )
        
        print("✅ All ranking files generated!")
    
    def save_ranking_file(self, rankings: List[Dict], filename_base: str, 
                         ranking_type: str, category: str):
        """Save individual ranking file"""
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 14,
                "ranking_type": ranking_type,
                "total_players": len(rankings)
            },
            "rankings": [
                {
                    "rank": i + 1,
                    **qb
                }
                for i, qb in enumerate(rankings)
            ]
        }
        
        filename = f"{filename_base}_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"   ✅ {filename}")
    
    def generate_comprehensive_analysis(self):
        """Main function to generate comprehensive QB analysis"""
        print("=" * 80)
        print("🏈 COMPREHENSIVE QB ANALYSIS GENERATOR - WEEK 14 (2025)")
        print("=" * 80)
        
        # Fetch all QB stats
        raw_stats = self.fetch_all_qb_stats()
        
        if not raw_stats:
            print("❌ Failed to fetch QB statistics")
            return
        
        # Process stats by player
        qb_data = self.process_qb_stats(raw_stats)
        
        # Calculate metrics
        qb_list = self.calculate_qb_metrics(qb_data)
        
        # Save comprehensive analysis file
        comprehensive_output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 14,
                "total_quarterbacks": len(qb_list),
                "data_source": "College Football Data API (GraphQL)"
            },
            "quarterbacks": qb_list
        }
        
        filename = f"comprehensive_qb_analysis_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(comprehensive_output, f, indent=2)
        
        print(f"\n💾 Comprehensive analysis saved: {filename}")
        
        # Generate all ranking files
        self.generate_rankings(qb_list)
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ QB ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"📊 Total QBs analyzed: {len(qb_list)}")
        print(f"📁 Files created: 6 (1 comprehensive + 5 rankings)")
        print("=" * 80)


def main():
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    analyzer = ComprehensiveQBAnalyzer(api_key, year=2025)
    analyzer.generate_comprehensive_analysis()


if __name__ == "__main__":
    main()
