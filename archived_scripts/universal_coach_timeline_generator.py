#!/usr/bin/env python3
"""
universal_coach_timeline_generator.py
Generates complete timeline JSON with auto-detected events, annotations, and zones
"""

import json
from datetime import datetime
from collections import defaultdict
from pathlib import Path

class UniversalCoachTimelineGenerator:
    def __init__(self, coach_name, master_data_path):
        """Load coach's master.json file"""
        with open(master_data_path, 'r') as f:
            self.data = json.load(f)
        self.coach_name = coach_name
        
    def generate_timeline(self):
        """Main orchestrator"""
        return {
            "metadata": self._extract_metadata(),
            "ranking_series": self._build_ranking_series(),
            "plot_bands": self._generate_plot_bands(),
            "annotations": self._detect_significant_events(),
            "stats_cards": self._generate_stat_cards(),
            "matchup_log": self._build_matchup_log(),
            "career_cards": self._generate_career_cards()
        }
    
    def _build_ranking_series(self):
        """Convert yearly_performance into Highcharts time series"""
        series = []
        
        if 'yearly_performance' not in self.data or 'seasons' not in self.data['yearly_performance']:
            print(f"⚠️  No yearly_performance data found for {self.coach_name}")
            return series
        
        for season in self.data['yearly_performance']['seasons']:
            year = season.get('year')
            if not year:
                continue
            
            # Pre-season (if ranked)
            if season.get('preseason_rank') and season['preseason_rank'] <= 25:
                series.append({
                    "date": f"{year}-08-01",
                    "rank": season['preseason_rank']
                })
            
            # Mid-season peak
            if season.get('peak_rank') and season['peak_rank'] <= 25:
                peak_week = season.get('peak_week', 7)
                month = 8 + (peak_week // 4)  # Estimate month
                series.append({
                    "date": f"{year}-{month:02d}-15",
                    "rank": season['peak_rank']
                })
            
            # End of season
            if season.get('final_rank') and season['final_rank'] <= 25:
                series.append({
                    "date": f"{year}-11-30",
                    "rank": season['final_rank']
                })
            else:
                # Unranked end (only add if we had earlier rankings this season)
                if season.get('preseason_rank') or season.get('peak_rank'):
                    series.append({
                        "date": f"{year}-11-30",
                        "rank": 26  # Below rankings
                    })
        
        return series
    
    def _generate_plot_bands(self):
        """Auto-generate color zones for each school"""
        bands = []
        
        for school_info in self.data.get('schools_info', []):
            school = school_info['name']
            years_str = school_info['years']
            
            # Handle different formats: "2009-2009", "2009 - 2013", "2020-Present"
            if ' - ' in years_str:
                years = years_str.split(' - ')
            elif '-' in years_str:
                years = years_str.split('-')
            else:
                years = [years_str, years_str]
            
            start_year = int(years[0])
            end_year = int(years[1]) if years[1] not in ['Present', 'present'] else datetime.now().year
            
            bands.append({
                "from": f"{start_year}-01-01",
                "to": f"{end_year}-12-31",
                "color": self._hex_to_rgba(school_info.get('primary_color', '#666699'), 0.05),
                "label": school_info.get('abbreviation', school[:4]).upper(),
                "labelColor": school_info.get('primary_color', '#666699')
            })
        
        return bands
    
    def _detect_significant_events(self):
        """AI-powered event detection from games/seasons"""
        annotations = []
        
        if 'yearly_performance' not in self.data or 'seasons' not in self.data['yearly_performance']:
            return annotations
        
        for season in self.data['yearly_performance']['seasons']:
            year = season.get('year')
            if not year:
                continue
                
            school = season.get('school', 'Unknown')
            school_info = self._get_school_info(school)
            
            # Event Detection Logic
            events = []
            
            # 1. Peak Ranking Achievement
            peak_rank = season.get('peak_rank', 26)
            if peak_rank <= 5:
                events.append({
                    "type": "peak_ranking",
                    "title": f"Reached #{peak_rank}",
                    "indicator": "↑",
                    "sentiment": "good",
                    "date": f"{year}-{8 + (season.get('peak_week', 7) // 4):02d}-15",
                    "rank": peak_rank,
                    "y_offset": -30
                })
            
            # 2. Preseason #1
            if season.get('preseason_rank') == 1:
                events.append({
                    "type": "preseason_one",
                    "title": "Preseason #1",
                    "indicator": "★",
                    "sentiment": "neutral",
                    "date": f"{year}-08-01",
                    "rank": 1,
                    "y_offset": -20
                })
            
            # 3. Bowl Games
            bowl = season.get('bowl_game') or season.get('bowl')
            if bowl:
                if isinstance(bowl, dict):
                    bowl_name = bowl.get('name', 'Bowl Game')
                    bowl_result = bowl.get('result', 'L')
                else:
                    bowl_name = 'Bowl Game'
                    bowl_result = 'L'
                
                events.append({
                    "type": "bowl",
                    "title": bowl_name,
                    "indicator": "★" if bowl_result == 'W' else "○",
                    "sentiment": "good" if bowl_result == 'W' else "neutral",
                    "date": f"{year}-12-20",
                    "rank": season.get('final_rank', 20),
                    "y_offset": 20
                })
            
            # 4. Record-Breaking Seasons
            wins = season.get('wins', 0)
            if wins >= 11:
                losses = season.get('losses', 0)
                events.append({
                    "type": "milestone",
                    "title": f"Best Season ({wins}-{losses})",
                    "indicator": "↑",
                    "sentiment": "good",
                    "date": f"{year}-11-01",
                    "rank": season.get('final_rank', 15),
                    "y_offset": -40
                })
            
            # 5. Conference Championships
            if season.get('conference_champ') or (season.get('achievements') and 'Conference' in str(season.get('achievements'))):
                events.append({
                    "type": "championship",
                    "title": "Conference Champion",
                    "indicator": "🏆",
                    "sentiment": "good",
                    "date": f"{year}-12-05",
                    "rank": season.get('final_rank', 10),
                    "y_offset": 30
                })
            
            # 6. Signature Wins (check vs_ranked if available)
            vs_ranked = season.get('vs_ranked', {})
            if isinstance(vs_ranked, dict):
                top5_wins = vs_ranked.get('vs_top_5', '0-0').split('-')[0]
                if top5_wins and int(top5_wins) > 0:
                    events.append({
                        "type": "signature_win",
                        "title": f"{top5_wins} Top 5 Win(s)",
                        "indicator": "★",
                        "sentiment": "good",
                        "date": f"{year}-10-15",
                        "rank": season.get('peak_rank', 15),
                        "y_offset": 30
                    })
            
            # Convert to annotations
            for event in events:
                annotations.append({
                    "x": event['date'],
                    "y": 26 - event['rank'],  # Inverted for chart
                    "text": self._build_annotation_html(event, school_info),
                    "yOffset": event['y_offset']
                })
        
        return annotations
    
    def _build_annotation_html(self, event, school_info):
        """Generate glassmorphism annotation HTML"""
        sentiment_class = f"text-{event['sentiment']}"
        logo = school_info.get('logo', '')
        
        return f'''<div class="chart-annotation">
            <img src="{logo}" class="annotation-team-logo">
            <div class="annotation-content">
                <span class="annotation-title">{event['title']}</span>
                <span class="annotation-indicator {sentiment_class}">{event['indicator']}</span>
            </div>
        </div>'''
    
    def _generate_stat_cards(self):
        """Auto-generate top stat cards for current tenure"""
        current_team = self.data.get('current_team', {})
        current_school_data = self._get_current_school_stats()
        
        cards = [
            {
                "label": "Tenure Record",
                "value": current_school_data['record'],
                "sub": current_school_data.get('peak_desc', 'Current Era'),
                "accent": self._school_to_accent(current_team.get('name', '')),
                "color": None
            },
            {
                "label": "Career Win %",
                "value": f"{current_school_data['career_win_pct']:.1f}%",
                "sub": f"{current_school_data['total_seasons']} Seasons",
                "accent": self._school_to_accent(current_team.get('name', '')),
                "color": current_team.get('primary_color')
            }
        ]
        
        # Add talent if available
        if current_school_data.get('latest_talent'):
            cards.insert(1, {
                "label": "Talent Composite",
                "value": str(current_school_data['latest_talent']),
                "sub": f"{current_school_data.get('talent_year', 2025)} Program Record",
                "accent": self._school_to_accent(current_team.get('name', '')),
                "color": current_team.get('primary_color')
            })
        
        # Add vs ranked if available
        if current_school_data.get('vs_ranked_record'):
            cards.append({
                "label": "Top 25 Record",
                "value": current_school_data['vs_ranked_record'],
                "sub": f"{current_school_data.get('vs_ranked_pct', 0):.1f}% Success Rate",
                "accent": self._school_to_accent(current_team.get('name', '')),
                "color": None
            })
        
        return cards
    
    def _build_matchup_log(self):
        """Extract all ranked opponent games from games array"""
        matchups = []
        
        # Get from games array - handle both dict and list structures
        games_data = self.data.get('games', [])
        if isinstance(games_data, dict):
            games = games_data.get('games', [])
        else:
            games = games_data
        
        for game in games:
            # Only include games where opponent was ranked
            if game.get('opponent_ranked') and game.get('opponent_rank'):
                opponent_rank = game['opponent_rank']
                
                # Generate contextual note
                note = self._generate_game_note(game)
                
                matchups.append({
                    "year": game.get('season', 'N/A'),
                    "school": game.get('school', 'N/A'),
                    "opponent": game.get('opponent', 'N/A'),
                    "rank": f"#{opponent_rank}",
                    "result": f"{game.get('result', 'L')} {game.get('score', '')}".strip(),
                    "note": note
                })
        
        # Sort by year descending
        matchups.sort(key=lambda x: x['year'] if isinstance(x['year'], int) else 0, reverse=True)
        
        return matchups
    
    def _generate_game_note(self, game):
        """Generate contextual note for a game"""
        notes = []
        
        # Check margin
        margin = game.get('margin', 0)
        if abs(margin) >= 20:
            if margin > 0:
                notes.append("Dominant Win")
            else:
                notes.append("Blowout Loss")
        elif abs(margin) <= 7:
            notes.append("Close Game")
        
        # Check location
        location = game.get('location', '')
        if location == 'Neutral':
            notes.append("Neutral Site")
        elif location == 'Away':
            notes.append("Road Win" if game.get('won') else "Road Loss")
        
        # Check season type
        if game.get('season_type') == 'postseason':
            notes.append("Bowl Game")
        
        # Check opponent rank
        opp_rank = game.get('opponent_rank', 26)
        if opp_rank <= 5:
            notes.append("Top 5 Opponent")
        elif opp_rank <= 10:
            notes.append("Top 10 Opponent")
        
        return ' • '.join(notes) if notes else '-'
    
    def _generate_career_cards(self):
        """Auto-generate cards for each school"""
        cards = []
        current_team_name = self.data.get('current_team', {}).get('name', '')
        
        for school_info in self.data.get('schools_info', []):
            if school_info['name'] == current_team_name:
                continue  # Skip current team (already in header)
            
            school_stats = self._get_school_specific_stats(school_info['name'])
            
            cards.append({
                "name": school_info['name'],
                "mascot": school_info.get('mascot', ''),
                "years": school_info['years'],
                "logo": school_info.get('logo', ''),
                "record": school_info.get('record', '0-0'),
                "accent": self._school_to_accent(school_info['name']),
                "stats": [
                    {
                        "label": "Record",
                        "value": school_info.get('record', '0-0')
                    },
                    {
                        "label": "Win %",
                        "value": f"{school_stats['win_pct']:.1f}%"
                    }
                ],
                "achievements": school_stats['highlights']
            })
        
        return cards
    
    def _hex_to_rgba(self, hex_color, alpha):
        """Convert hex to rgba"""
        if not hex_color:
            hex_color = '#666699'
        hex_color = hex_color.lstrip('#')
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r}, {g}, {b}, {alpha})"
        except:
            return f"rgba(102, 102, 153, {alpha})"
    
    # Helper methods
    def _get_school_info(self, school_name):
        for school in self.data.get('schools_info', []):
            if school['name'] == school_name:
                return school
        return {'logo': '', 'primary_color': '#666699'}
    
    def _get_current_school_stats(self):
        """Get stats for current school"""
        current_team = self.data.get('current_team', {})
        current_school = current_team.get('name', '')
        summary = self.data.get('summary', {})
        
        # Get current school from schools_info
        current_school_info = None
        for school in self.data.get('schools_info', []):
            if school['name'] == current_school:
                current_school_info = school
                break
        
        record = current_school_info['record'] if current_school_info else summary.get('career_record', '0-0')
        
        # Parse record
        parts = record.split('-')
        wins = int(parts[0]) if len(parts) > 0 else 0
        losses = int(parts[1]) if len(parts) > 1 else 0
        total = wins + losses
        win_pct = (wins / total * 100) if total > 0 else 0
        
        # Get talent data
        talent_data = self.data.get('talent_and_development', {})
        latest_talent = None
        talent_year = None
        
        if 'talent_composite' in talent_data:
            for school_talent in talent_data['talent_composite']:
                if school_talent['school'] == current_school:
                    by_year = school_talent.get('by_year', [])
                    if by_year:
                        latest = by_year[-1]
                        latest_talent = round(latest.get('talent', 0), 2)
                        talent_year = latest.get('year', 2025)
                    break
        
        # Get vs ranked record from career_stats
        vs_ranked_record = None
        vs_ranked_pct = 0
        career_stats = self.data.get('career_stats', {})
        
        # Get overall vs_ranked data (encompasses all schools)
        vs_ranked = career_stats.get('vs_ranked', {})
        vs_ranked_record = vs_ranked.get('overall', '0-0')
        
        # Calculate percentage
        parts = vs_ranked_record.split('-')
        if len(parts) == 2:
            rw = int(parts[0])
            rl = int(parts[1])
            rt = rw + rl
            vs_ranked_pct = (rw / rt * 100) if rt > 0 else 0
        
        return {
            'record': record,
            'win_pct': win_pct,
            'peak_desc': f"{win_pct:.1f}% Win Rate",
            'career_win_pct': summary.get('career_win_pct', win_pct),
            'total_seasons': summary.get('total_seasons', 0),
            'latest_talent': latest_talent,
            'talent_year': talent_year,
            'vs_ranked_record': vs_ranked_record,
            'vs_ranked_pct': vs_ranked_pct
        }
    
    def _get_school_specific_stats(self, school_name):
        """Get detailed stats for a specific school"""
        # Find school in schools_info
        school_info = None
        for school in self.data.get('schools_info', []):
            if school['name'] == school_name:
                school_info = school
                break
        
        if not school_info:
            return {'win_pct': 0, 'highlights': []}
        
        # Parse record
        record = school_info.get('record', '0-0')
        parts = record.split('-')
        wins = int(parts[0]) if len(parts) > 0 else 0
        losses = int(parts[1]) if len(parts) > 1 else 0
        total = wins + losses
        win_pct = (wins / total * 100) if total > 0 else 0
        
        # Generate highlights from yearly performance
        highlights = []
        years_str = school_info.get('years', '')
        
        # Handle different formats
        if ' - ' in years_str:
            years = years_str.split(' - ')
        elif '-' in years_str:
            years = years_str.split('-')
        else:
            years = [years_str, years_str]
            
        start_year = int(years[0]) if years and years[0].isdigit() else 0
        end_year_str = years[1] if len(years) > 1 else years[0]
        end_year = int(end_year_str) if end_year_str.isdigit() else datetime.now().year
        
        # Find best season and generate highlights
        best_wins = 0
        best_season = None
        bowl_appearances = 0
        ranked_wins = 0
        
        if 'yearly_performance' in self.data:
            for season in self.data['yearly_performance'].get('seasons', []):
                if season.get('school') == school_name:
                    wins = season.get('wins', 0)
                    if wins > best_wins:
                        best_wins = wins
                        best_season = season
                    
                    # Count bowl appearances
                    if season.get('bowl_game') or season.get('bowl'):
                        bowl_appearances += 1
        
        # Count ranked wins from games
        games_data = self.data.get('games', [])
        if isinstance(games_data, dict):
            games = games_data.get('games', [])
        else:
            games = games_data
            
        for game in games:
            if isinstance(game, dict) and game.get('school') == school_name and game.get('opponent_ranked') and game.get('won'):
                ranked_wins += 1
        
        # Build highlights
        if best_season:
            highlights.append(f"{best_season['wins']}-{best_season['losses']} Record ({best_season['year']})")
        
        if bowl_appearances > 0:
            highlights.append(f"{bowl_appearances} Bowl Appearance{'s' if bowl_appearances > 1 else ''}")
        
        if ranked_wins > 0:
            highlights.append(f"{ranked_wins} Win{'s' if ranked_wins > 1 else ''} vs Ranked Teams")
        
        if win_pct > 70:
            highlights.append(f"Elite {win_pct:.1f}% Win Rate")
        elif win_pct > 60:
            highlights.append(f"Strong {win_pct:.1f}% Win Rate")
        
        tenure_years = end_year - start_year + 1
        if tenure_years >= 3 and not any('Year' in h for h in highlights):
            highlights.append(f"{tenure_years} Season{'s' if tenure_years > 1 else ''} of Leadership")
        
        # Ensure at least 3 highlights
        if len(highlights) == 0:
            highlights.append(f"{record} Overall Record")
        if len(highlights) == 1:
            highlights.append("Program Development")
        if len(highlights) == 2:
            highlights.append("Competitive Performance")
        
        return {
            'win_pct': win_pct,
            'highlights': highlights[:5]  # Max 5 highlights
        }
    
    def _school_to_accent(self, school_name):
        """Map school name to CSS accent class"""
        mapping = {
            'Ole Miss': 'olemiss',
            'Florida Atlantic': 'fau',
            'USC': 'usc',
            'Tennessee': 'tenn',
            'Penn State': 'pennstate',
            'Vanderbilt': 'vandy',
            'Notre Dame': 'notredame',
            'LSU': 'lsu'
        }
        return mapping.get(school_name, 'default')
    
    def _extract_metadata(self):
        """Extract metadata"""
        total_seasons = len(self.data.get('yearly_performance', {}).get('seasons', []))
        
        return {
            "coach": self.coach_name,
            "generated": datetime.now().isoformat(),
            "total_seasons": total_seasons,
            "current_team": self.data.get('current_team', {}).get('name', 'Unknown')
        }


# Test with Lane Kiffin and James Franklin
if __name__ == "__main__":
    coaches = [
        {
            "name": "Lane Kiffin",
            "file": "frontend/src/data/lane_kiffin_master.json"
        },
        {
            "name": "James Franklin",
            "file": "frontend/src/data/james_franklin_master.json"
        }
    ]
    
    output_dir = Path("frontend/src/data/timelines")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("🚀 UNIVERSAL COACH TIMELINE GENERATOR")
    print("=" * 80)
    
    for coach in coaches:
        print(f"\n📊 Processing: {coach['name']}")
        print("-" * 80)
        
        master_path = coach['file']
        if not Path(master_path).exists():
            print(f"❌ Master file not found: {master_path}")
            continue
        
        try:
            generator = UniversalCoachTimelineGenerator(
                coach_name=coach['name'],
                master_data_path=master_path
            )
            
            timeline_data = generator.generate_timeline()
            
            # Save to JSON
            slug = coach['name'].lower().replace(' ', '_')
            output_path = output_dir / f"{slug}_timeline.json"
            
            with open(output_path, 'w') as f:
                json.dump(timeline_data, f, indent=2)
            
            # Print summary
            print(f"✅ Timeline Generated: {output_path}")
            print(f"   📈 Ranking Points: {len(timeline_data['ranking_series'])}")
            print(f"   📍 Annotations: {len(timeline_data['annotations'])}")
            print(f"   🏫 Plot Bands: {len(timeline_data['plot_bands'])}")
            print(f"   📊 Stat Cards: {len(timeline_data['stats_cards'])}")
            print(f"   🎯 Matchup Log: {len(timeline_data['matchup_log'])} games")
            print(f"   🏈 Career Cards: {len(timeline_data['career_cards'])} schools")
            
        except Exception as e:
            print(f"❌ Error processing {coach['name']}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ GENERATION COMPLETE")
    print("=" * 80)
