#!/usr/bin/env python3
"""
Display Ohio State vs Michigan Week 14 Prediction
Shows the three key UI sections: Win Probability, Final Prediction, ATS Comparison, Market Analysis
"""

import requests
import json
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def display_prediction():
    """Fetch and display Ohio State vs Michigan prediction"""
    
    url = "http://localhost:5002/predict"
    payload = {
        "home_team": "Michigan",
        "away_team": "Ohio State"
    }
    
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}OHIO STATE vs MICHIGAN - WEEK 14 2025 PREDICTION")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    try:
        print(f"{Fore.YELLOW}⏳ Fetching prediction data (this may take 60-90 seconds)...\n")
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        ui = data.get('ui_components', {})
        
        # Header Information
        header = ui.get('header', {})
        game_info = header.get('game_info', {})
        print(f"{Fore.WHITE}Date: {Fore.GREEN}{game_info.get('date', 'N/A')}")
        print(f"{Fore.WHITE}Time: {Fore.GREEN}{game_info.get('time', 'N/A')}")
        print(f"{Fore.WHITE}Network: {Fore.GREEN}{game_info.get('network', 'N/A')}")
        print(f"{Fore.WHITE}Excitement: {Fore.YELLOW}{game_info.get('excitement_index', 0):.1f}/5 ⭐")
        
        # Section 1: Win Probability & Prediction Cards
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}1. WIN PROBABILITY & PREDICTION CARDS")
        print(f"{Fore.CYAN}{'='*80}")
        
        pred_cards = ui.get('prediction_cards', {})
        win_prob = pred_cards.get('win_probability', {})
        
        print(f"\n{Fore.YELLOW}🎯 Win Probability:")
        print(f"{Fore.WHITE}   {win_prob.get('favored_team', '')} {Fore.GREEN}favored")
        print(f"{Fore.WHITE}   Home (Michigan): {Fore.CYAN}{win_prob.get('home_team_prob', 0):.1f}%")
        print(f"{Fore.WHITE}   Away (Ohio State): {Fore.RED}{win_prob.get('away_team_prob', 0):.1f}%")
        
        spread = pred_cards.get('predicted_spread', {})
        print(f"\n{Fore.YELLOW}📊 Predicted Spread: {Fore.GREEN}{spread.get('model_spread_display', '')}")
        print(f"{Fore.WHITE}   Wins by: {Fore.CYAN}{abs(spread.get('model_spread', 0)):.1f} pts")
        print(f"{Fore.WHITE}   Market: {Fore.MAGENTA}{spread.get('market_spread', 0):.1f}")
        print(f"{Fore.WHITE}   Edge: {Fore.YELLOW}{spread.get('edge', 0):.1f}pt")
        
        total = pred_cards.get('predicted_total', {})
        print(f"\n{Fore.YELLOW}🔢 Predicted Total: {Fore.GREEN}{total.get('model_total', 0):.1f}")
        print(f"{Fore.WHITE}   Model: {Fore.CYAN}{total.get('model_total', 0):.1f}")
        print(f"{Fore.WHITE}   Market: {Fore.MAGENTA}{total.get('market_total', 0):.1f}")
        print(f"{Fore.WHITE}   Edge: {Fore.YELLOW}{total.get('edge', 0):.1f}")
        
        # Section 2: Final Prediction Summary
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}2. FINAL PREDICTION SUMMARY")
        print(f"{Fore.CYAN}{'='*80}")
        
        final_pred = ui.get('final_prediction', {})
        score = final_pred.get('predicted_score', {})
        
        print(f"\n{Fore.YELLOW}📍 Final Score Prediction:")
        away_score = score.get('away_score', 0)
        home_score = score.get('home_score', 0)
        winner_color = Fore.GREEN if away_score > home_score else Fore.WHITE
        loser_color = Fore.WHITE if away_score > home_score else Fore.GREEN
        
        print(f"{winner_color}   {score.get('away_team', 'Ohio State')}: {away_score}")
        print(f"{loser_color}   {score.get('home_team', 'Michigan')}: {home_score}")
        print(f"{Fore.CYAN}   Total: {score.get('total', 0)}")
        
        print(f"\n{Fore.YELLOW}🔑 Key Factors:")
        for i, factor in enumerate(final_pred.get('key_factors', []), 1):
            print(f"{Fore.WHITE}   {i}. {factor}")
        
        # Section 3: Against The Spread (ATS) Performance
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}3. AGAINST THE SPREAD (ATS) PERFORMANCE")
        print(f"{Fore.CYAN}{'='*80}")
        
        ats_comp = ui.get('ats_comparison', {})
        away_ats = ats_comp.get('away_team', {})
        home_ats = ats_comp.get('home_team', {})
        
        print(f"\n{Fore.RED}🏈 Ohio State (Away):")
        print(f"{Fore.WHITE}   ATS Record: {Fore.CYAN}{away_ats.get('ats_record', 'N/A')}")
        print(f"{Fore.WHITE}   Cover Rate: {Fore.GREEN}{away_ats.get('cover_rate', 0):.1f}% {Fore.YELLOW}- {away_ats.get('rating', 'N/A')}")
        print(f"{Fore.WHITE}   Avg Cover Margin: {Fore.MAGENTA}{away_ats.get('avg_cover_margin', 0):.1f}")
        
        print(f"\n{Fore.BLUE}🏈 Michigan (Home):")
        print(f"{Fore.WHITE}   ATS Record: {Fore.CYAN}{home_ats.get('ats_record', 'N/A')}")
        print(f"{Fore.WHITE}   Cover Rate: {Fore.GREEN}{home_ats.get('cover_rate', 0):.1f}% {Fore.YELLOW}- {home_ats.get('rating', 'N/A')}")
        print(f"{Fore.WHITE}   Avg Cover Margin: {Fore.MAGENTA}{home_ats.get('avg_cover_margin', 0):.1f}")
        
        print(f"\n{Fore.YELLOW}💡 ATS Betting Intelligence:")
        print(f"{Fore.WHITE}   {ats_comp.get('betting_intelligence', 'N/A')}")
        
        # Section 4: Market Comparison & Sportsbook Lines
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}4. MARKET COMPARISON & LIVE SPORTSBOOK LINES")
        print(f"{Fore.CYAN}{'='*80}")
        
        betting = ui.get('detailed_analysis', {}).get('betting_analysis', {})
        
        print(f"\n{Fore.YELLOW}📈 Market Value Analysis:")
        print(f"{Fore.WHITE}   Model Spread: {Fore.GREEN}{spread.get('model_spread_display', '')}")
        print(f"{Fore.WHITE}   Market Spread: {Fore.MAGENTA}{betting.get('formatted_spread', 'N/A')}")
        print(f"{Fore.WHITE}   Spread Edge: {Fore.YELLOW}{betting.get('spread_edge', 0):.1f}pt")
        print(f"{Fore.WHITE}   Total Edge: {Fore.YELLOW}{betting.get('total_edge', 0):.1f}")
        
        print(f"\n{Fore.GREEN}💰 Recommended Bets:")
        spread_rec = betting.get('spread_recommendation', 'No edge')
        spread_edge = betting.get('spread_edge', 0)
        edge_color = Fore.GREEN if abs(spread_edge) >= 2 else Fore.YELLOW
        print(f"{Fore.WHITE}   Spread: {edge_color}{spread_rec}")
        if spread_edge:
            print(f"{Fore.WHITE}           {edge_color}({abs(spread_edge):.1f}PT EDGE)")
        
        total_rec = betting.get('total_recommendation', 'No edge')
        total_edge_val = betting.get('total_edge', 0)
        total_edge_color = Fore.GREEN if abs(total_edge_val) >= 3 else Fore.YELLOW
        print(f"{Fore.WHITE}   Total:  {total_edge_color}{total_rec}")
        if total_edge_val:
            print(f"{Fore.WHITE}           {total_edge_color}({abs(total_edge_val):.1f}PT EDGE)")
        
        sportsbooks = betting.get('sportsbooks', {}).get('individual_books', [])
        if sportsbooks:
            print(f"\n{Fore.YELLOW}🎰 Live Sportsbook Lines:")
            for book in sportsbooks[:3]:
                print(f"{Fore.WHITE}   {Fore.CYAN}{book.get('name', 'N/A'):12s}{Fore.WHITE}: {Fore.MAGENTA}{book.get('spread_display', 'N/A'):20s} {Fore.WHITE}Total: {Fore.GREEN}{book.get('total', 0)}")
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ COMPREHENSIVE ANALYSIS COMPLETE!")
        print(f"{Fore.CYAN}{'='*80}\n")
        
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Error: Could not connect to Flask server at {url}")
        print(f"{Fore.YELLOW}💡 Make sure the backend is running: python app.py")
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}❌ Error: Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"{Fore.RED}❌ HTTP Error: {e}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    display_prediction()
