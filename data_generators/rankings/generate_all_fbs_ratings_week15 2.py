#!/usr/bin/env python3
"""
Generate All FBS Ratings Files for Week 15
==========================================
Creates individual rating files for:
- ELO rankings
- FPI rankings  
- SP+ rankings
- SRS rankings
- Combined comprehensive ratings

All data for 2025 season through Week 15
"""

import requests
import json
from datetime import datetime
from typing import Dict, List
import time

class AllFBSRatingsGenerator:
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
    
    def fetch_all_ratings(self) -> List[Dict]:
        """Fetch all FBS team ratings"""
        print("📊 Fetching all FBS team ratings...")
        
        query = """
        query GetAllRatings($year: smallint!) {
          ratings(where: {year: {_eq: $year}}, orderBy: {elo: DESC}) {
            team
            teamId
            year
            conference
            conferenceId
            elo
            fpi
            fpiOffensiveEfficiency
            fpiDefensiveEfficiency
            fpiSpecialTeamsEfficiency
            fpiOverallEfficiency
            fpiSosRank
            fpiRemainingSosRank
            fpiStrengthOfRecordRank
            fpiResumeRank
            fpiGameControlRank
            fpiAvgWinProbabilityRank
            spOverall
            spOffense
            spDefense
            spSpecialTeams
            srs
          }
        }
        """
        
        variables = {"year": self.year}
        data = self.execute_query(query, variables)
        
        if data and "ratings" in data:
            ratings = data["ratings"]
            print(f"✅ Fetched ratings for {len(ratings)} teams")
            return ratings
        
        return []
    
    def generate_elo_rankings(self, all_ratings: List[Dict]) -> str:
        """Generate ELO rankings file"""
        print("\n📈 Generating ELO rankings...")
        
        # Sort by ELO (descending)
        elo_ratings = sorted(
            [r for r in all_ratings if r.get('elo')],
            key=lambda x: x['elo'],
            reverse=True
        )
        
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 15,
                "total_teams": len(elo_ratings),
                "rating_system": "ELO"
            },
            "ratings": [
                {
                    "rank": i + 1,
                    "team": r["team"],
                    "conference": r.get("conference"),
                    "elo": round(r["elo"], 1)
                }
                for i, r in enumerate(elo_ratings)
            ]
        }
        
        filename = f"fbs_elo_rankings_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return filename
    
    def generate_fpi_rankings(self, all_ratings: List[Dict]) -> str:
        """Generate FPI rankings file"""
        print("\n📈 Generating FPI rankings...")
        
        # Sort by FPI (descending)
        fpi_ratings = sorted(
            [r for r in all_ratings if r.get('fpi') is not None],
            key=lambda x: x['fpi'],
            reverse=True
        )
        
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 15,
                "total_teams": len(fpi_ratings),
                "rating_system": "FPI (Football Power Index)"
            },
            "ratings": [
                {
                    "rank": i + 1,
                    "team": r["team"],
                    "conference": r.get("conference"),
                    "fpi": round(r["fpi"], 2),
                    "offensive_efficiency": round(r.get("fpiOffensiveEfficiency", 0), 2) if r.get("fpiOffensiveEfficiency") else None,
                    "defensive_efficiency": round(r.get("fpiDefensiveEfficiency", 0), 2) if r.get("fpiDefensiveEfficiency") else None,
                    "special_teams_efficiency": round(r.get("fpiSpecialTeamsEfficiency", 0), 2) if r.get("fpiSpecialTeamsEfficiency") else None,
                    "resume_rank": r.get("fpiResumeRank")
                }
                for i, r in enumerate(fpi_ratings)
            ]
        }
        
        filename = f"fbs_fpi_rankings_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return filename
    
    def generate_sp_rankings(self, all_ratings: List[Dict]) -> str:
        """Generate SP+ rankings file"""
        print("\n📈 Generating SP+ rankings...")
        
        # Sort by SP+ Overall (descending)
        sp_ratings = sorted(
            [r for r in all_ratings if r.get('spOverall') is not None],
            key=lambda x: x['spOverall'],
            reverse=True
        )
        
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 15,
                "total_teams": len(sp_ratings),
                "rating_system": "SP+ (Success Rate Plus)"
            },
            "ratings": [
                {
                    "rank": i + 1,
                    "team": r["team"],
                    "conference": r.get("conference"),
                    "sp_overall": round(r["spOverall"], 1),
                    "sp_offense": round(r.get("spOffense", 0), 1) if r.get("spOffense") else None,
                    "sp_defense": round(r.get("spDefense", 0), 1) if r.get("spDefense") else None,
                    "sp_special_teams": round(r.get("spSpecialTeams", 0), 1) if r.get("spSpecialTeams") else None
                }
                for i, r in enumerate(sp_ratings)
            ]
        }
        
        filename = f"fbs_sp_overall_rankings_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return filename
    
    def generate_srs_rankings(self, all_ratings: List[Dict]) -> str:
        """Generate SRS rankings file"""
        print("\n📈 Generating SRS rankings...")
        
        # Sort by SRS (descending)
        srs_ratings = sorted(
            [r for r in all_ratings if r.get('srs') is not None],
            key=lambda x: x['srs'],
            reverse=True
        )
        
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 15,
                "total_teams": len(srs_ratings),
                "rating_system": "SRS (Simple Rating System)"
            },
            "ratings": [
                {
                    "rank": i + 1,
                    "team": r["team"],
                    "conference": r.get("conference"),
                    "srs": round(r["srs"], 1)
                }
                for i, r in enumerate(srs_ratings)
            ]
        }
        
        filename = f"fbs_srs_rankings_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return filename
    
    def generate_comprehensive_ratings(self, all_ratings: List[Dict]) -> str:
        """Generate comprehensive combined ratings file"""
        print("\n📈 Generating comprehensive ratings (all systems)...")
        
        # Create comprehensive dataset
        comprehensive_teams = []
        
        for r in all_ratings:
            team_data = {
                "team": r["team"],
                "conference": r.get("conference"),
                "team_id": r.get("teamId"),
                "ratings": {
                    "elo": round(r.get("elo", 0), 1) if r.get("elo") else None,
                    "fpi": round(r.get("fpi", 0), 2) if r.get("fpi") is not None else None,
                    "sp_overall": round(r.get("spOverall", 0), 1) if r.get("spOverall") is not None else None,
                    "srs": round(r.get("srs", 0), 1) if r.get("srs") is not None else None
                },
                "fpi_details": {
                    "offensive_efficiency": round(r.get("fpiOffensiveEfficiency", 0), 2) if r.get("fpiOffensiveEfficiency") else None,
                    "defensive_efficiency": round(r.get("fpiDefensiveEfficiency", 0), 2) if r.get("fpiDefensiveEfficiency") else None,
                    "special_teams_efficiency": round(r.get("fpiSpecialTeamsEfficiency", 0), 2) if r.get("fpiSpecialTeamsEfficiency") else None,
                    "sos_rank": r.get("fpiSosRank"),
                    "resume_rank": r.get("fpiResumeRank")
                },
                "sp_details": {
                    "offense": round(r.get("spOffense", 0), 1) if r.get("spOffense") else None,
                    "defense": round(r.get("spDefense", 0), 1) if r.get("spDefense") else None,
                    "special_teams": round(r.get("spSpecialTeams", 0), 1) if r.get("spSpecialTeams") else None
                }
            }
            
            # Calculate composite score (average of normalized ratings where available)
            ratings_for_composite = []
            if team_data["ratings"]["elo"]:
                ratings_for_composite.append(team_data["ratings"]["elo"] / 20)  # Normalize to ~0-100
            if team_data["ratings"]["fpi"] is not None:
                ratings_for_composite.append((team_data["ratings"]["fpi"] + 20) * 2)  # Normalize to ~0-100
            if team_data["ratings"]["sp_overall"] is not None:
                ratings_for_composite.append((team_data["ratings"]["sp_overall"] + 20) * 2)  # Normalize to ~0-100
            if team_data["ratings"]["srs"] is not None:
                ratings_for_composite.append((team_data["ratings"]["srs"] + 20) * 2)  # Normalize to ~0-100
            
            if ratings_for_composite:
                team_data["composite_score"] = round(sum(ratings_for_composite) / len(ratings_for_composite), 2)
            else:
                team_data["composite_score"] = 0
            
            comprehensive_teams.append(team_data)
        
        # Sort by composite score
        comprehensive_teams.sort(key=lambda x: x["composite_score"], reverse=True)
        
        # Add composite rank
        for i, team in enumerate(comprehensive_teams):
            team["composite_rank"] = i + 1
        
        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "season": self.year,
                "week": 15,
                "total_teams": len(comprehensive_teams),
                "rating_systems": ["ELO", "FPI", "SP+", "SRS"],
                "composite_methodology": "Normalized average of all available rating systems"
            },
            "teams": comprehensive_teams
        }
        
        filename = f"all_fbs_ratings_comprehensive_2025_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        return filename
    
    def generate_all(self):
        """Generate all rating files"""
        print("=" * 80)
        print("🏈 ALL FBS RATINGS GENERATOR - WEEK 15 (2025)")
        print("=" * 80)
        
        # Fetch all ratings data
        all_ratings = self.fetch_all_ratings()
        
        if not all_ratings:
            print("❌ Failed to fetch ratings data")
            return
        
        # Generate individual rating files
        files_created = []
        
        files_created.append(self.generate_elo_rankings(all_ratings))
        files_created.append(self.generate_fpi_rankings(all_ratings))
        files_created.append(self.generate_sp_rankings(all_ratings))
        files_created.append(self.generate_srs_rankings(all_ratings))
        files_created.append(self.generate_comprehensive_ratings(all_ratings))
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ ALL RATINGS FILES GENERATED")
        print("=" * 80)
        print(f"📁 Files created: {len(files_created)}")
        for f in files_created:
            print(f"   - {f}")
        print("=" * 80)


def main():
    api_key = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"
    generator = AllFBSRatingsGenerator(api_key, year=2025)
    generator.generate_all()


if __name__ == "__main__":
    main()
