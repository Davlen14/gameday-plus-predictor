#!/usr/bin/env python3
"""
🚀 NUCLEAR CFP PREDICTOR - DYNAMIC COLAB INTERFACE 🚀
=======================================================
Use your trained 4.76M datapoint model to predict ANY matchup instantly!

USAGE IN COLAB:
1. Upload this file to Colab
2. Load your saved model: load_nuclear_model()
3. Predict any matchup: predict_matchup("Oregon", "Georgia")
4. Get detailed analysis: analyze_matchup("Indiana", "Ole Miss")

📊 Powered by 4,758,555 datapoints across 3 databases
⚡ Nuclear ensemble with RandomForest + GradientBoosting + LogisticRegression
"""

import sqlite3
import pandas as pd
import numpy as np
import pickle
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import ML models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

class NuclearCFPPredictor:
    """🚀 Dynamic Nuclear CFP Predictor - Trained on 4.76M datapoints"""
    
    def __init__(self):
        self.models = {}
        self.feature_columns = []
        self.team_mapping = {}
        self.databases = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        self.total_datapoints = 4758555
        print("🚀 Nuclear CFP Predictor Initialized")
        print(f"⚡ Ready to process {self.total_datapoints:,} datapoints")
    
    def connect_databases(self, playoff_db_path, coaches_db_path, predictions_db_path):
        """🔗 Connect to all three nuclear databases"""
        try:
            self.databases = {
                'playoff': sqlite3.connect(playoff_db_path),
                'coaches': sqlite3.connect(coaches_db_path), 
                'predictions': sqlite3.connect(predictions_db_path)
            }
            print("✅ ALL THREE NUCLEAR DATABASES CONNECTED")
            print(f"   🏈 PLAYOFF: {playoff_db_path}")
            print(f"   👨‍💼 COACHES: {coaches_db_path}")
            print(f"   🔮 PREDICTIONS: {predictions_db_path}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def save_model(self, model_path="nuclear_cfp_model.pkl"):
        """💾 Save trained nuclear model for instant loading"""
        if not self.is_trained:
            print("❌ No trained model to save!")
            return False
        
        try:
            model_data = {
                'models': self.models,
                'feature_columns': self.feature_columns,
                'team_mapping': self.team_mapping,
                'scaler': self.scaler,
                'total_datapoints': self.total_datapoints,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Nuclear model saved to {model_path}")
            print(f"📊 Features: {len(self.feature_columns)}")
            print(f"⚡ Datapoints: {self.total_datapoints:,}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save model: {e}")
            return False
    
    def load_model(self, model_path="nuclear_cfp_model.pkl"):
        """⚡ Load pre-trained nuclear model for instant predictions"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.models = model_data['models']
            self.feature_columns = model_data['feature_columns']
            self.team_mapping = model_data['team_mapping']
            self.scaler = model_data['scaler']
            self.total_datapoints = model_data['total_datapoints']
            self.is_trained = True
            
            print("🚀 NUCLEAR MODEL LOADED SUCCESSFULLY!")
            print(f"📊 Features: {len(self.feature_columns)}")
            print(f"⚡ Training Datapoints: {self.total_datapoints:,}")
            print(f"🤖 Models: {list(self.models.keys())}")
            print(f"📅 Trained: {model_data.get('timestamp', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            print("💡 Make sure you've saved your trained model first!")
            return False
    
    def get_team_features(self, team_name):
        """📊 Extract comprehensive features for any team from all 3 databases"""
        features = {}
        
        try:
            # Database 1: CFP Team Analysis Features
            playoff_conn = self.databases.get('playoff')
            if playoff_conn:
                # CFP team stats
                cfp_query = """
                SELECT * FROM cfp_teams 
                WHERE team = ? OR team LIKE ?
                LIMIT 1
                """
                cfp_data = pd.read_sql_query(cfp_query, playoff_conn, params=[team_name, f'%{team_name}%'])
                
                if not cfp_data.empty:
                    for col in cfp_data.columns:
                        if col != 'team':
                            features[f'cfp_{col}'] = cfp_data.iloc[0][col]
                
                # Drive-level features
                drive_query = """
                SELECT 
                    AVG(yards) as avg_drive_yards,
                    AVG(plays) as avg_drive_plays,
                    COUNT(*) as total_drives,
                    SUM(CASE WHEN result = 'TD' THEN 1 ELSE 0 END) as touchdown_drives,
                    SUM(CASE WHEN result = 'FG' THEN 1 ELSE 0 END) as field_goal_drives
                FROM cfp_drives 
                WHERE team = ? OR team LIKE ?
                """
                drive_data = pd.read_sql_query(drive_query, playoff_conn, params=[team_name, f'%{team_name}%'])
                
                if not drive_data.empty:
                    for col in drive_data.columns:
                        features[f'drive_{col}'] = drive_data.iloc[0][col]
            
            # Database 2: Coaching Intelligence Features
            coaches_conn = self.databases.get('coaches')
            if coaches_conn:
                # Coaching stats
                coach_query = """
                SELECT 
                    seasons_experience,
                    career_wins,
                    career_losses,
                    bowl_wins,
                    conference_championships
                FROM coaches 
                WHERE school = ? OR school LIKE ?
                ORDER BY seasons_experience DESC
                LIMIT 1
                """
                coach_data = pd.read_sql_query(coach_query, coaches_conn, params=[team_name, f'%{team_name}%'])
                
                if not coach_data.empty:
                    for col in coach_data.columns:
                        features[f'coach_{col}'] = coach_data.iloc[0][col]
                
                # Situational stats
                sit_query = """
                SELECT 
                    blowout_wins,
                    close_wins,
                    comeback_wins,
                    vs_ranked_wins
                FROM situational_stats 
                WHERE school = ? OR school LIKE ?
                LIMIT 1
                """
                sit_data = pd.read_sql_query(sit_query, coaches_conn, params=[team_name, f'%{team_name}%'])
                
                if not sit_data.empty:
                    for col in sit_data.columns:
                        features[f'sit_{col}'] = sit_data.iloc[0][col]
                
                # Recruiting data
                rec_query = """
                SELECT 
                    AVG(avg_rating) as avg_recruiting_rating,
                    AVG(total_commits) as avg_commits,
                    COUNT(*) as recruiting_classes
                FROM recruiting_classes 
                WHERE school = ? OR school LIKE ?
                """
                rec_data = pd.read_sql_query(rec_query, coaches_conn, params=[team_name, f'%{team_name}%'])
                
                if not rec_data.empty:
                    for col in rec_data.columns:
                        features[f'rec_{col}'] = rec_data.iloc[0][col]
            
            # Database 3: Advanced Analytics Features
            pred_conn = self.databases.get('predictions')
            if pred_conn:
                # EPA metrics
                epa_query = """
                SELECT * FROM team_epa_stats 
                WHERE team = ? OR team LIKE ?
                LIMIT 1
                """
                epa_data = pd.read_sql_query(epa_query, pred_conn, params=[team_name, f'%{team_name}%'])
                
                if not epa_data.empty:
                    for col in epa_data.columns:
                        if col != 'team':
                            features[f'epa_{col}'] = epa_data.iloc[0][col]
                
                # Power rankings
                power_query = """
                SELECT * FROM team_power_rankings 
                WHERE team = ? OR team LIKE ?
                LIMIT 1
                """
                power_data = pd.read_sql_query(power_query, pred_conn, params=[team_name, f'%{team_name}%'])
                
                if not power_data.empty:
                    for col in power_data.columns:
                        if col != 'team':
                            features[f'power_{col}'] = power_data.iloc[0][col]
            
            # Fill missing values with defaults
            for feature in self.feature_columns:
                if feature not in features:
                    if 'home' in feature.lower():
                        features[feature] = 0  # Neutral site default
                    elif 'neutral' in feature.lower():
                        features[feature] = 1  # Assume neutral site
                    else:
                        features[feature] = 0  # Default to 0
            
            return features
            
        except Exception as e:
            print(f"⚠️ Error extracting features for {team_name}: {e}")
            # Return default features if extraction fails
            default_features = {col: 0 for col in self.feature_columns}
            return default_features
    
    def predict_matchup(self, home_team, away_team, neutral_site=True, verbose=True):
        """🎯 Predict any CFP matchup using nuclear model"""
        if not self.is_trained:
            print("❌ Model not loaded! Use load_model() first.")
            return None
        
        try:
            # Get features for both teams
            home_features = self.get_team_features(home_team)
            away_features = self.get_team_features(away_team)
            
            # Create differential features (how nuclear model was trained)
            game_features = {}
            
            # Home field advantage
            game_features['is_home'] = 0 if neutral_site else 1
            game_features['is_neutral'] = 1 if neutral_site else 0
            
            # Calculate differentials for all matching features
            for feature in self.feature_columns:
                if feature in ['is_home', 'is_neutral']:
                    continue
                
                # Extract base feature name (remove diff_ prefix if exists)
                base_feature = feature.replace('diff_off_norm_', '').replace('diff_off_raw_', '')
                base_feature = base_feature.replace('diff_def_norm_', '').replace('diff_def_raw_', '')
                
                # Find matching features in team data
                home_val = 0
                away_val = 0
                
                # Try different feature name patterns
                possible_names = [
                    base_feature,
                    f'cfp_{base_feature}',
                    f'epa_{base_feature}',
                    f'power_{base_feature}',
                    f'drive_{base_feature}',
                    f'coach_{base_feature}',
                    f'sit_{base_feature}',
                    f'rec_{base_feature}'
                ]
                
                for name in possible_names:
                    if name in home_features:
                        home_val = home_features[name] or 0
                        break
                
                for name in possible_names:
                    if name in away_features:
                        away_val = away_features[name] or 0
                        break
                
                # Calculate differential
                game_features[feature] = home_val - away_val
            
            # Ensure we have all required features
            feature_vector = []
            for col in self.feature_columns:
                feature_vector.append(game_features.get(col, 0))
            
            # Convert to DataFrame for prediction
            X = pd.DataFrame([feature_vector], columns=self.feature_columns)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Get predictions from all models
            predictions = {}
            probabilities = {}
            
            for name, model in self.models.items():
                pred = model.predict(X_scaled)[0]
                prob = model.predict_proba(X_scaled)[0]
                predictions[name] = pred
                probabilities[name] = prob[1] if len(prob) > 1 else prob[0]
            
            # Ensemble prediction (majority vote + average probability)
            ensemble_pred = np.mean(list(predictions.values())) > 0.5
            ensemble_prob = np.mean(list(probabilities.values()))
            
            # Determine winner and confidence
            if ensemble_pred:
                winner = home_team
                confidence = ensemble_prob * 100
            else:
                winner = away_team
                confidence = (1 - ensemble_prob) * 100
            
            if verbose:
                print("\n🏈 --- NUCLEAR CFP PREDICTION --- 🏈")
                print(f"📊 Using {self.total_datapoints:,} datapoints • 3 databases")
                print(f"⚡ {home_team} vs {away_team}")
                print(f"🏟️ Venue: {'Neutral Site' if neutral_site else home_team + ' (Home)'}")
                print(f"\n🤖 Individual Model Predictions:")
                for name, prob in probabilities.items():
                    pred_team = home_team if prob > 0.5 else away_team
                    pred_conf = (prob if prob > 0.5 else 1-prob) * 100
                    print(f"   {name}: {pred_team} ({pred_conf:.1f}%)")
                
                print(f"\n🏆 NUCLEAR ENSEMBLE PREDICTION:")
                print(f"   Winner: {winner}")
                print(f"   Confidence: {confidence:.1f}%")
                print(f"   {home_team} Win Probability: {ensemble_prob*100:.1f}%")
                print(f"   {away_team} Win Probability: {(1-ensemble_prob)*100:.1f}%")
            
            return {
                'winner': winner,
                'confidence': confidence,
                'home_win_prob': ensemble_prob,
                'away_win_prob': 1 - ensemble_prob,
                'individual_predictions': predictions,
                'individual_probabilities': probabilities,
                'matchup': f"{home_team} vs {away_team}",
                'venue': 'Neutral Site' if neutral_site else f"{home_team} (Home)"
            }
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return None
    
    def analyze_bracket(self, bracket_teams, verbose=True):
        """🏆 Analyze entire CFP bracket using nuclear model"""
        if not isinstance(bracket_teams, list) or len(bracket_teams) != 12:
            print("❌ Bracket must be a list of 12 teams")
            return None
        
        if verbose:
            print("🏆 --- NUCLEAR CFP BRACKET ANALYSIS --- 🏆")
            print(f"📊 Processing {len(bracket_teams)} teams with {self.total_datapoints:,} datapoints\n")
        
        results = {}
        
        # First Round (Campus Sites)
        first_round = [
            (bracket_teams[11], bracket_teams[4]),  # 12 @ 5
            (bracket_teams[10], bracket_teams[5]),  # 11 @ 6  
            (bracket_teams[9], bracket_teams[6]),   # 10 @ 7
            (bracket_teams[8], bracket_teams[7])    # 9 @ 8
        ]
        
        first_round_winners = []
        if verbose:
            print("--- FIRST ROUND (Campus Sites) ---")
        
        for away, home in first_round:
            pred = self.predict_matchup(home, away, neutral_site=False, verbose=False)
            winner = pred['winner']
            confidence = pred['confidence']
            first_round_winners.append(winner)
            
            if verbose:
                seed_away = bracket_teams.index(away) + 1
                seed_home = bracket_teams.index(home) + 1
                print(f"#{seed_away} {away} @ #{seed_home} {home} → {winner} ({confidence:.1f}%)")
        
        # Quarterfinals (New Year's Six Bowls)
        quarterfinals = [
            (first_round_winners[3], bracket_teams[0]),  # Winner vs #1
            (first_round_winners[0], bracket_teams[3]),  # Winner vs #4
            (first_round_winners[1], bracket_teams[2]),  # Winner vs #3
            (first_round_winners[2], bracket_teams[1])   # Winner vs #2
        ]
        
        quarterfinal_winners = []
        if verbose:
            print("\n--- QUARTERFINALS (New Year's Six Bowls) ---")
        
        bowl_names = ["Rose Bowl", "Sugar Bowl", "Peach Bowl", "Cotton Bowl"]
        for i, (team1, team2) in enumerate(quarterfinals):
            pred = self.predict_matchup(team2, team1, neutral_site=True, verbose=False)
            winner = pred['winner']
            confidence = pred['confidence']
            quarterfinal_winners.append(winner)
            
            if verbose:
                print(f"{bowl_names[i]}: {team1} vs {team2} → {winner} ({confidence:.1f}%)")
        
        # Semifinals
        semifinals = [
            (quarterfinal_winners[0], quarterfinal_winners[1]),
            (quarterfinal_winners[2], quarterfinal_winners[3])
        ]
        
        semifinal_winners = []
        if verbose:
            print("\n--- SEMIFINALS ---")
        
        for i, (team1, team2) in enumerate(semifinals):
            pred = self.predict_matchup(team1, team2, neutral_site=True, verbose=False)
            winner = pred['winner']
            confidence = pred['confidence']
            semifinal_winners.append(winner)
            
            if verbose:
                print(f"Semifinal {i+1}: {team1} vs {team2} → {winner} ({confidence:.1f}%)")
        
        # Championship
        championship = (semifinal_winners[0], semifinal_winners[1])
        champ_pred = self.predict_matchup(championship[0], championship[1], neutral_site=True, verbose=False)
        champion = champ_pred['winner']
        champ_confidence = champ_pred['confidence']
        
        if verbose:
            print(f"\n--- 🏆 ULTIMATE CFP CHAMPIONSHIP 🏆 ---")
            print(f"🏆 CHAMPION: {championship[0]} vs {championship[1]} → {champion} ({champ_confidence:.1f}%)")
        
        results = {
            'first_round_winners': first_round_winners,
            'quarterfinal_winners': quarterfinal_winners,
            'semifinal_winners': semifinal_winners,
            'champion': champion,
            'championship_confidence': champ_confidence,
            'championship_matchup': championship
        }
        
        return results
    
    def quick_predict(self, team1, team2):
        """⚡ Quick prediction without verbose output"""
        return self.predict_matchup(team1, team2, verbose=False)
    
    def get_team_strength(self, team_name):
        """💪 Get team strength rating from nuclear model"""
        if not self.is_trained:
            return None
        
        # Simulate matchup against average team to get strength
        features = self.get_team_features(team_name)
        
        # Calculate composite strength from key features
        strength_features = [
            'cfp_total_yards', 'epa_offense', 'epa_defense',
            'power_overall_rating', 'coach_career_wins', 'rec_avg_recruiting_rating'
        ]
        
        strength_score = 0
        valid_features = 0
        
        for feature in strength_features:
            if feature in features and features[feature] is not None:
                strength_score += features[feature]
                valid_features += 1
        
        if valid_features > 0:
            normalized_strength = (strength_score / valid_features) / 100 * 85 + 15  # Scale to 15-100
            return min(max(normalized_strength, 15), 100)
        
        return 50  # Default average rating

# ============================================================================
# 🚀 COLAB QUICK FUNCTIONS - Copy these to your Colab notebook!
# ============================================================================

# Global predictor instance
nuclear_predictor = NuclearCFPPredictor()

def setup_nuclear_predictor(playoff_db, coaches_db, predictions_db):
    """🔗 Quick setup for Colab - connects all databases"""
    global nuclear_predictor
    return nuclear_predictor.connect_databases(playoff_db, coaches_db, predictions_db)

def save_nuclear_model(path="nuclear_cfp_model.pkl"):
    """💾 Save your trained model"""
    global nuclear_predictor
    return nuclear_predictor.save_model(path)

def load_nuclear_model(path="nuclear_cfp_model.pkl"):
    """⚡ Load your trained model"""
    global nuclear_predictor
    return nuclear_predictor.load_model(path)

def predict_matchup(team1, team2, neutral=True):
    """🎯 Predict any matchup instantly!"""
    global nuclear_predictor
    return nuclear_predictor.predict_matchup(team1, team2, neutral_site=neutral)

def quick_predict(team1, team2):
    """⚡ Quick prediction without verbose output"""
    global nuclear_predictor
    return nuclear_predictor.quick_predict(team1, team2)

def predict_bracket(teams):
    """🏆 Predict entire CFP bracket"""
    global nuclear_predictor
    return nuclear_predictor.analyze_bracket(teams)

def team_strength(team_name):
    """💪 Get team strength rating (0-100)"""
    global nuclear_predictor
    return nuclear_predictor.get_team_strength(team_name)

def nuclear_status():
    """📊 Check nuclear predictor status"""
    global nuclear_predictor
    print(f"🚀 Nuclear CFP Predictor Status:")
    print(f"   Trained: {'✅' if nuclear_predictor.is_trained else '❌'}")
    print(f"   Datapoints: {nuclear_predictor.total_datapoints:,}")
    print(f"   Features: {len(nuclear_predictor.feature_columns)}")
    print(f"   Models: {len(nuclear_predictor.models)}")

# ============================================================================
# 🎯 EXAMPLE USAGE FOR COLAB
# ============================================================================

def demo_predictions():
    """🎯 Demo nuclear predictions"""
    print("🚀 NUCLEAR CFP PREDICTOR DEMO")
    print("=" * 50)
    
    # Check if model is loaded
    if not nuclear_predictor.is_trained:
        print("❌ Please load your trained model first:")
        print("   load_nuclear_model('your_model.pkl')")
        return
    
    # Demo matchups
    demo_matchups = [
        ("Oregon", "Georgia"),
        ("Indiana", "Ole Miss"), 
        ("Texas", "Penn State"),
        ("Notre Dame", "Alabama"),
        ("Ohio State", "Texas A&M")
    ]
    
    print("🏈 NUCLEAR PREDICTIONS:")
    for team1, team2 in demo_matchups:
        result = quick_predict(team1, team2)
        if result:
            print(f"   {team1} vs {team2}: {result['winner']} ({result['confidence']:.1f}%)")
    
    print("\n💪 TEAM STRENGTH RATINGS:")
    demo_teams = ["Oregon", "Georgia", "Indiana", "Ole Miss", "Texas"]
    for team in demo_teams:
        strength = team_strength(team)
        print(f"   {team}: {strength:.1f}/100")

if __name__ == "__main__":
    print("🚀 Nuclear CFP Predictor Dynamic Interface Loaded!")
    print("\n📋 QUICK START IN COLAB:")
    print("1. setup_nuclear_predictor(playoff_db, coaches_db, predictions_db)")
    print("2. load_nuclear_model('your_saved_model.pkl')")
    print("3. predict_matchup('Oregon', 'Georgia')")
    print("4. predict_bracket(['Indiana', 'Oregon', 'Georgia', ...])")
    print("\n⚡ Use demo_predictions() to test with sample matchups!")