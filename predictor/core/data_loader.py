import json
import os
from typing import Dict, List, Any

class DataLoader:
    """Handles loading of all static JSON data files"""
    
    def __init__(self):
        self.static_data = {}
    
    def _load_all_static_data(self) -> Dict:
        """Load all static JSON data files for comprehensive team analysis"""
        try:
            # Base path for data files
            base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            
            # Load comprehensive team stats
            with open(os.path.join(base_path, 'fbs_teams_stats_only.json'), 'r') as f:
                fbs_stats = json.load(f)
            
            # Load Power 5 efficiency data
            with open(os.path.join(base_path, 'react_power5_efficiency.json'), 'r') as f:
                power5_efficiency = json.load(f)
            
            # Load drive-level data
            with open(os.path.join(base_path, 'power5_drives_only.json'), 'r') as f:
                drive_data = json.load(f)
            
            # Load historical win probabilities for calibration
            with open(os.path.join(base_path, 'complete_win_probabilities.json'), 'r') as f:
                historical_probs = json.load(f)
            
            # Load AP and Coaches poll data
            with open(os.path.join(base_path, 'ap.json'), 'r') as f:
                ap_polls = json.load(f)
            
            with open(os.path.join(base_path, 'coaches_simplified_ranked.json'), 'r') as f:
                coaches_polls = json.load(f)
            
            # Load conference and ranking data
            with open(os.path.join(base_path, 'react_fbs_conferences.json'), 'r') as f:
                conference_data = json.load(f)
            
            with open(os.path.join(base_path, 'react_fbs_team_rankings.json'), 'r') as f:
                team_rankings = json.load(f)
            
            # Load season summaries
            with open(os.path.join(base_path, 'team_season_summaries_clean.json'), 'r') as f:
                season_summaries = json.load(f)
            
            # Load elite coaching data with vs ranked stats
            coaches_path = os.path.join(base_path, 'coaches_with_vsranked_stats.json')
            with open(coaches_path, 'r') as f:
                coaches_data = json.load(f)
            
            # ENHANCED DATA LOADING - New files for improved accuracy
            
            # Load team-organized Power 5 drives for better drive analysis
            with open(os.path.join(base_path, 'react_power5_teams.json'), 'r') as f:
                power5_teams_drives = json.load(f)
            
            # Load structured offensive stats with metadata
            with open(os.path.join(base_path, 'fbs_offensive_stats.json'), 'r') as f:
                structured_offensive_stats = json.load(f)
            
            # Load structured defensive stats with metadata
            with open(os.path.join(base_path, 'fbs_defensive_stats.json'), 'r') as f:
                structured_defensive_stats = json.load(f)
            
            # Load backtesting data if available for enhanced calibration
            backtesting_data = {}
            try:
                # Try the new backtesting 2 directory first
                backtesting_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backtesting 2')
                if not os.path.exists(backtesting_path):
                    # Fallback to old backtesting directory
                    backtesting_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backtesting')
                
                for filename in os.listdir(backtesting_path):
                    if filename.startswith('all_fbs_ratings_comprehensive') and filename.endswith('.json'):
                        with open(os.path.join(backtesting_path, filename), 'r') as f:
                            backtesting_data = json.load(f)
                        print(f"✅ Loaded backtesting data from {filename}")
                        break
            except Exception as e:
                print(f"⚠️  Backtesting data not found - using standard calibration: {e}")
            
            # Import processing methods from data_processor
            from ..utils.data_processor import DataProcessor
            processor = DataProcessor()
            
            # Process and organize data
            return {
                'team_stats': processor._process_team_stats(fbs_stats),
                'efficiency': power5_efficiency,
                'drives': processor._process_drive_data(drive_data),
                'historical_probs': historical_probs,
                'ap_polls': ap_polls,
                'coaches_polls': coaches_polls,
                'conferences': conference_data,
                'rankings': team_rankings,
                'season_summaries': season_summaries,
                'team_name_to_id': processor._create_team_lookup(fbs_stats),
                'coaches_raw': coaches_data,
                'coaching_data': processor._extract_coaching_data(coaches_data),
                # Enhanced data additions
                'power5_teams_drives': processor._process_team_drives(power5_teams_drives),
                'structured_offensive': processor._process_structured_offensive(structured_offensive_stats),
                'structured_defensive': processor._process_structured_defensive(structured_defensive_stats),
                'backtesting_ratings': processor._process_backtesting_data(backtesting_data)
            }
        except Exception as e:
            print(f"⚠️  Warning: Could not load static data files: {e}")
            print("   Prediction will work with real-time data only")
            return {}
    
    async def load_all_static_data(self) -> Dict:
        """Async wrapper for static data loading"""
        if not self.static_data:
            self.static_data = self._load_all_static_data()
        return self.static_data
    
    def _load_comprehensive_player_data(self) -> Dict[str, Any]:
        """Load comprehensive player analysis files from backtesting 2/ directory"""
        import json
        
        # Player data file paths - all in data/ folder now
        player_files = {
            'qbs': 'data/comprehensive_qb_analysis_2025_20251015_034259.json',
            'rbs': 'data/comprehensive_rb_analysis_2025_20251015_043434.json', 
            'wrs': 'data/comprehensive_wr_analysis_2025_20251015_045922.json',
            'tes': 'data/comprehensive_te_analysis_2025_20251015_050510.json',
            'dbs': 'data/comprehensive_db_analysis_2025_20251015_051747.json',
            'lbs': 'data/comprehensive_lb_analysis_2025_20251015_053156.json',
            'dls': 'data/comprehensive_dl_analysis_2025_20251015_051056.json'
        }
        
        player_data = {}
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        
        for position, filename in player_files.items():
            try:
                file_path = os.path.join(base_dir, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    player_data[position] = data
                    print(f"✅ Loaded {position.upper()} data: {len(data.get('players', []))} players")
                else:
                    print(f"⚠️  Player file not found: {filename}")
                    player_data[position] = {'players': []}
            except Exception as e:
                print(f"❌ Error loading {position} data: {e}")
                player_data[position] = {'players': []}
        
        return player_data