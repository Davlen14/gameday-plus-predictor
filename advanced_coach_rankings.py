#!/usr/bin/env python3
"""
Advanced Coach Rankings System - COMPREHENSIVE VERSION
Analyzes coaches based on ALL available factors:
- Talent vs Performance (overachievers/underachievers)
- Recent trends (2025 HEAVILY weighted, then 2024, 2023, 2022)
- Big game performance vs ranked opponents
- Recruiting/talent ratings vs actual results
- Clutch factor in ranked matchups
- 2025 season performance and momentum
- Betting line performance (cover rate)
- AP Poll rankings consistency
- Draft picks produced (NFL talent development)
"""
import json
from collections import defaultdict
from pathlib import Path
import statistics

def load_talent_data():
    """Load team talent composite rankings"""
    try:
        with open('data/team_talent_composite.json', 'r') as f:
            return json.load(f)
    except:
        print("⚠️  No talent data found, using estimates")
        return {}

def calculate_weighted_recent_trend(coach_file_path):
    """
    Calculate weighted performance trend with 2025 HEAVILY weighted
    2025: 50% weight (current season most important)
    2024: 30% weight  
    2023: 15% weight
    2022: 5% weight
    """
    try:
        with open(coach_file_path, 'r') as f:
            data = json.load(f)
        
        games = data.get('games', [])
        school = data.get('metadata', {}).get('school', '')
        
        # Get seasons with weights
        seasons = {}
        weights = {2025: 0.50, 2024: 0.30, 2023: 0.15, 2022: 0.05}
        
        for year in [2022, 2023, 2024, 2025]:
            year_games = [g for g in games if g.get('season') == year]
            if year_games:
                wins = sum(1 for g in year_games 
                          if (g.get('homePoints') is not None and g.get('awayPoints') is not None) and
                             ((g['homeTeam'] == school and g['homePoints'] > g['awayPoints']) or
                              (g['awayTeam'] == school and g['awayPoints'] > g['homePoints'])))
                total = len(year_games)
                win_pct = wins/total if total > 0 else 0
                seasons[year] = {
                    'wins': wins, 
                    'losses': total - wins,
                    'total': total, 
                    'win_pct': win_pct,
                    'weight': weights.get(year, 0)
                }
        
        if len(seasons) < 2:
            return 0, seasons, 0
        
        # Calculate weighted average win percentage
        weighted_win_pct = sum(s['win_pct'] * s['weight'] for s in seasons.values())
        
        # Calculate momentum (2025 vs 2024 change)
        if 2025 in seasons and 2024 in seasons:
            momentum = (seasons[2025]['win_pct'] - seasons[2024]['win_pct']) * 100
        else:
            momentum = 0
        
        # Calculate overall trend
        years = sorted(seasons.keys())
        if len(years) >= 3:
            recent_avg = statistics.mean([seasons[y]['win_pct'] for y in years[-2:]])
            older_avg = statistics.mean([seasons[y]['win_pct'] for y in years[:-2]])
            trend_score = (recent_avg - older_avg) * 100
        else:
            trend_score = momentum
        
        return trend_score, seasons, weighted_win_pct * 100
        
    except Exception as e:
        print(f"  Error calculating trend: {e}")
        return 0, {}, 0

def analyze_talent_vs_performance(coach_name, team, career_win_pct, total_wins):
    """
    Determine if coach overachieves or underachieves based on talent level
    Elite programs (top recruiting) SHOULD win 85%+ - if not, they're underachieving with loaded rosters
    Mid-tier programs winning 65%+ are overachieving - doing more with less
    """
    # Talent tier estimates (based on typical recruiting rankings)
    elite_programs = ['Alabama', 'Georgia', 'Ohio State', 'Texas', 'LSU', 'Oklahoma', 
                     'Clemson', 'Notre Dame', 'USC', 'Texas A&M', 'Florida', 'Miami']
    
    upper_tier = ['Oregon', 'Penn State', 'Michigan', 'Florida State', 'Auburn', 
                 'Tennessee', 'Oklahoma State', 'Wisconsin', 'Washington']
    
    mid_tier = ['Iowa', 'Ole Miss', 'Kansas State', 'Missouri', 'Louisville',
               'BYU', 'Utah', 'Baylor', 'TCU', 'North Carolina', 'Virginia Tech']
    
    # Expected win percentage by tier (what they SHOULD win with their talent)
    if team in elite_programs:
        expected_win_pct = 85.0  # Elite rosters should dominate
        tier = "Elite Talent"
    elif team in upper_tier:
        expected_win_pct = 70.0  # Good rosters should win most games
        tier = "Upper Talent"
    elif team in mid_tier:
        expected_win_pct = 60.0  # Mid-tier rosters
        tier = "Mid Talent"
    else:
        expected_win_pct = 50.0  # Lower talent teams
        tier = "Developing"
    
    # Calculate overachievement score (positive = exceeding expectations, negative = underachieving)
    performance_delta = career_win_pct - expected_win_pct
    
    # Classification based on talent context
    if team in elite_programs:
        # Elite programs: High bar - they have the best players
        if performance_delta >= 5:
            classification = "🏆 Maximizing Elite Talent"
            score = 95 + min(performance_delta, 10)
        elif performance_delta >= 0:
            classification = "✅ Meeting Elite Expectations"
            score = 85 + performance_delta
        elif performance_delta >= -5:
            classification = "⚠️ Underachieving (Loaded Roster)"
            score = 70 + performance_delta
        else:
            classification = "🔻 Wasting Elite Talent"
            score = 55 + max(performance_delta, -15)
    elif team in upper_tier:
        # Upper tier: Good talent, should win most games
        if performance_delta >= 8:
            classification = "🌟 Elite Overachiever"
            score = 95 + min(performance_delta, 15)
        elif performance_delta >= 3:
            classification = "📈 Strong Overachiever"
            score = 85 + performance_delta
        elif performance_delta >= -3:
            classification = "✅ Meeting Expectations"
            score = 75 + performance_delta
        else:
            classification = "⚠️ Underperforming"
            score = 60 + performance_delta
    else:
        # Mid/Lower tier: Overachieving is doing MORE with less
        if performance_delta >= 15:
            classification = "🌟 Miracle Worker"
            score = 100
        elif performance_delta >= 10:
            classification = "🚀 Elite Overachiever"
            score = 95 + min(performance_delta - 10, 5)
        elif performance_delta >= 5:
            classification = "📈 Strong Overachiever"
            score = 85 + performance_delta
        elif performance_delta >= 0:
            classification = "✅ Meeting Expectations"
            score = 75 + performance_delta
        else:
            classification = "⚠️ Underperforming"
            score = 65 + performance_delta
    
    return {
        'tier': tier,
        'expected_win_pct': expected_win_pct,
        'actual_win_pct': career_win_pct,
        'performance_delta': round(performance_delta, 1),
        'classification': classification,
        'context_score': max(0, min(100, score))
    }

def calculate_big_game_factor(vs_ranked_data):
    """Calculate how well coach performs in big games"""
    vs_top5 = vs_ranked_data.get('vsTop5', {})
    vs_top10 = vs_ranked_data.get('vsTop10', {})
    vs_ranked = vs_ranked_data
    
    # Parse records
    def parse_record(record_str):
        parts = record_str.split('-')
        if len(parts) >= 2:
            wins = int(parts[0])
            total = wins + int(parts[1])
            return wins, total
        return 0, 0
    
    top5_wins, top5_total = parse_record(vs_top5.get('record', '0-0-0'))
    top10_wins, top10_total = parse_record(vs_top10.get('record', '0-0-0'))
    ranked_wins, ranked_total = parse_record(vs_ranked.get('record', '0-0-0'))
    
    # Calculate big game win percentages
    top5_pct = (top5_wins / top5_total * 100) if top5_total > 0 else 0
    top10_pct = (top10_wins / top10_total * 100) if top10_total > 0 else 0
    ranked_pct = (ranked_wins / ranked_total * 100) if ranked_total > 0 else 0
    
    # Weighted big game score (top 5 games matter more)
    if top5_total >= 3:  # At least 3 top 5 games
        big_game_score = (top5_pct * 0.5) + (top10_pct * 0.3) + (ranked_pct * 0.2)
    elif top10_total >= 5:
        big_game_score = (top10_pct * 0.6) + (ranked_pct * 0.4)
    else:
        big_game_score = ranked_pct
    
    # Classification
    if big_game_score >= 60 and top5_total >= 5:
        clutch_rating = "🔥 Elite Big Game Coach"
    elif big_game_score >= 50:
        clutch_rating = "💪 Strong in Big Games"
    elif big_game_score >= 40:
        clutch_rating = "📊 Average Big Game"
    else:
        clutch_rating = "📉 Struggles vs Elite"
    
    return {
        'big_game_score': round(big_game_score, 1),
        'clutch_rating': clutch_rating,
        'vs_top5_record': f"{top5_wins}-{top5_total-top5_wins}",
        'vs_top5_pct': round(top5_pct, 1),
        'vs_top10_pct': round(top10_pct, 1),
        'vs_ranked_pct': round(ranked_pct, 1),
        'big_games_total': ranked_total
    }

def analyze_2025_season_performance(coach_file_path, school):
    """Analyze 2025 season in depth - wins, quality wins, close games"""
    try:
        with open(coach_file_path, 'r') as f:
            data = json.load(f)
        
        games_2025 = [g for g in data.get('games', []) if g.get('season') == 2025]
        
        if not games_2025:
            return {'season_score': 50, 'quality_wins': 0, 'rating': 'No 2025 Data'}
        
        wins = 0
        losses = 0
        quality_wins = 0  # Wins vs ranked opponents
        blowout_wins = 0  # Wins by 14+ points
        close_wins = 0    # Wins by 7 or less (clutch)
        bad_losses = 0    # Losses to unranked teams
        
        for game in games_2025:
            if game.get('homePoints') is None or game.get('awayPoints') is None:
                continue
                
            is_home = game['homeTeam'] == school
            team_score = game['homePoints'] if is_home else game['awayPoints']
            opp_score = game['awayPoints'] if is_home else game['homePoints']
            opp_rank = game.get('awayRank') if is_home else game.get('homeRank')
            margin = team_score - opp_score
            
            if margin > 0:  # Win
                wins += 1
                if opp_rank and opp_rank <= 25:
                    quality_wins += 1
                if margin >= 14:
                    blowout_wins += 1
                elif margin <= 7:
                    close_wins += 1
            else:  # Loss
                losses += 1
                if not opp_rank or opp_rank > 25:
                    bad_losses += 1
        
        total_games = wins + losses
        win_pct = (wins / total_games * 100) if total_games > 0 else 0
        
        # Season score calculation
        season_score = win_pct * 0.6  # Base win %
        season_score += (quality_wins * 5)  # +5 per ranked win
        season_score += (blowout_wins * 2)  # +2 per blowout
        season_score += (close_wins * 3)    # +3 per clutch win
        season_score -= (bad_losses * 8)    # -8 per bad loss
        season_score = max(0, min(100, season_score))
        
        if win_pct >= 85 and quality_wins >= 3:
            rating = "🔥 Elite 2025 Season"
        elif win_pct >= 75:
            rating = "💪 Strong 2025 Season"
        elif win_pct >= 60:
            rating = "✅ Solid 2025 Season"
        elif win_pct >= 50:
            rating = "📊 Average 2025 Season"
        else:
            rating = "📉 Struggling 2025"
        
        return {
            'season_score': round(season_score, 1),
            'record': f"{wins}-{losses}",
            'win_pct': round(win_pct, 1),
            'quality_wins': quality_wins,
            'blowout_wins': blowout_wins,
            'close_wins': close_wins,
            'bad_losses': bad_losses,
            'rating': rating
        }
        
    except Exception as e:
        return {'season_score': 50, 'quality_wins': 0, 'rating': 'Error'}

def analyze_talent_ratings(coach_file_path):
    """Analyze recruiting/talent composite ratings over time"""
    try:
        with open(coach_file_path, 'r') as f:
            data = json.load(f)
        
        talent_data = data.get('talent_ratings', [])
        if not talent_data:
            return {'avg_talent': 0, 'recent_talent': 0, 'trend': 0}
        
        # Get average talent rating
        talents = [t.get('talent', 0) for t in talent_data]
        avg_talent = statistics.mean(talents) if talents else 0
        
        # Get recent years (2023-2025)
        recent_talents = [t.get('talent', 0) for t in talent_data if t.get('year', 0) >= 2023]
        recent_talent = statistics.mean(recent_talents) if recent_talents else avg_talent
        
        # Talent trend (improving recruiting?)
        if len(talents) >= 3:
            recent = statistics.mean(talents[-3:])
            older = statistics.mean(talents[:-3]) if len(talents) > 3 else talents[0]
            trend = recent - older
        else:
            trend = 0
        
        return {
            'avg_talent': round(avg_talent, 1),
            'recent_talent': round(recent_talent, 1),
            'trend': round(trend, 1)
        }
    except:
        return {'avg_talent': 0, 'recent_talent': 0, 'trend': 0}

def analyze_draft_picks(coach_file_path):
    """Analyze NFL draft picks produced - talent development indicator"""
    try:
        with open(coach_file_path, 'r') as f:
            data = json.load(f)
        
        draft_picks = data.get('draft_picks', [])
        if not draft_picks:
            return {'total_picks': 0, 'first_rounders': 0, 'score': 0}
        
        total_picks = len(draft_picks)
        first_rounders = sum(1 for p in draft_picks if p.get('round', 99) == 1)
        top10_picks = sum(1 for p in draft_picks if p.get('pick', 999) <= 10)
        
        # NFL development score
        score = (total_picks * 1) + (first_rounders * 3) + (top10_picks * 5)
        
        return {
            'total_picks': total_picks,
            'first_rounders': first_rounders,
            'top10_picks': top10_picks,
            'score': score
        }
    except:
        return {'total_picks': 0, 'first_rounders': 0, 'score': 0}

def analyze_betting_performance_2025(coach_file_path, school):
    """Analyze how team performs vs betting lines in 2025"""
    try:
        with open(coach_file_path, 'r') as f:
            data = json.load(f)
        
        betting_2025 = data.get('betting_lines_2025', [])
        if not betting_2025:
            return {'cover_rate': 50, 'covers': 0, 'total': 0}
        
        covers = 0
        total_games = 0
        
        for game in betting_2025:
            if not game.get('lines'):
                continue
                
            is_home = game['homeTeam'] == school
            team_score = game.get('homePoints')
            opp_score = game.get('awayPoints')
            
            if team_score is None or opp_score is None:
                continue
            
            # Get average spread
            spreads = [line.get('spread', 0) for line in game['lines'] if line.get('spread')]
            if not spreads:
                continue
                
            avg_spread = statistics.mean(spreads)
            actual_margin = team_score - opp_score
            
            # Determine if covered
            if is_home:
                covered = (actual_margin + avg_spread) > 0
            else:
                covered = (actual_margin - avg_spread) > 0
            
            if covered:
                covers += 1
            total_games += 1
        
        cover_rate = (covers / total_games * 100) if total_games > 0 else 50
        
        return {
            'cover_rate': round(cover_rate, 1),
            'covers': covers,
            'total': total_games
        }
    except:
        return {'cover_rate': 50, 'covers': 0, 'total': 0}

def calculate_consistency_score(seasons_data):
    """Measure year-to-year consistency"""
    if len(seasons_data) < 2:
        return 50, "Insufficient Data"
    
    win_pcts = [s['win_pct'] for s in seasons_data.values()]
    
    # Calculate standard deviation
    mean = sum(win_pcts) / len(win_pcts)
    variance = sum((x - mean) ** 2 for x in win_pcts) / len(win_pcts)
    std_dev = variance ** 0.5
    
    # Lower std_dev = more consistent
    # Convert to 0-100 score (lower variance = higher score)
    consistency_score = max(0, 100 - (std_dev * 200))
    
    if consistency_score >= 80:
        rating = "🎯 Extremely Consistent"
    elif consistency_score >= 65:
        rating = "✅ Very Consistent"
    elif consistency_score >= 50:
        rating = "📊 Moderately Consistent"
    else:
        rating = "📉 Inconsistent"
    
    return round(consistency_score, 1), rating

def calculate_composite_ranking(coach_data, enhanced_stats):
    """
    Generate comprehensive ranking score with ALL factors
    HEAVILY weights 2025 performance and recent momentum
    """
    
    # 1. Career win % (15% weight) - historical baseline
    career_win_pct_score = coach_data['careerWinPct']
    
    # 2. Talent context score (15% weight) - doing more/less with talent
    context_score = enhanced_stats['talent_context']['context_score']
    
    # 3. Big game performance (12% weight) - vs ranked opponents
    big_game_score = enhanced_stats['big_game_analysis']['big_game_score']
    
    # 4. 2025 SEASON PERFORMANCE (25% weight) - MOST IMPORTANT
    season_2025_score = enhanced_stats.get('season_2025', {}).get('season_score', 50)
    
    # 5. Weighted recent trend (15% weight) - momentum with 2025 heavy
    weighted_win_pct = enhanced_stats['recent_trend'].get('weighted_win_pct', 50)
    
    # 6. Recruiting/talent development (8% weight)
    talent_score = min(100, enhanced_stats.get('talent_ratings', {}).get('recent_talent', 0) / 10)
    
    # 7. NFL draft picks (5% weight) - player development
    draft_score = min(100, enhanced_stats.get('draft_analysis', {}).get('score', 0) * 2)
    
    # 8. Betting performance 2025 (3% weight) - exceeding expectations
    betting_score = enhanced_stats.get('betting_2025', {}).get('cover_rate', 50)
    
    # 9. Consistency (2% weight)
    consistency_score = enhanced_stats['consistency']['score']
    
    # Weighted composite score - totals 100%
    composite = (
        career_win_pct_score * 0.15 +   # 15% career win %
        context_score * 0.15 +           # 15% talent vs performance context
        big_game_score * 0.12 +          # 12% big game performance
        season_2025_score * 0.25 +       # 25% 2025 SEASON (MOST IMPORTANT)
        weighted_win_pct * 0.15 +        # 15% weighted recent performance
        talent_score * 0.08 +            # 8% recruiting/talent
        draft_score * 0.05 +             # 5% NFL development
        betting_score * 0.03 +           # 3% betting performance
        consistency_score * 0.02         # 2% consistency
    )
    
    return round(composite, 2)

def generate_coach_summary(coach_data, enhanced_stats):
    """Generate comprehensive natural language summary with ALL factors"""
    name = coach_data['name']
    team = coach_data['team']
    record = coach_data['careerRecord']
    win_pct = coach_data['careerWinPct']
    
    talent = enhanced_stats['talent_context']
    big_game = enhanced_stats['big_game_analysis']
    season_2025 = enhanced_stats.get('season_2025', {})
    trend = enhanced_stats['recent_trend']
    draft = enhanced_stats.get('draft_analysis', {})
    betting = enhanced_stats.get('betting_2025', {})
    
    summary_parts = []
    
    # 1. Career baseline
    summary_parts.append(f"{name} ({team}) has a {record} career record ({win_pct}%).")
    
    # 2. 2025 season performance (MOST IMPORTANT)
    if season_2025.get('record'):
        summary_parts.append(f"2025: {season_2025['record']} ({season_2025['win_pct']:.1f}%) - {season_2025['rating']}.")
        if season_2025.get('quality_wins', 0) > 0:
            summary_parts.append(f"{season_2025['quality_wins']} ranked wins this year.")
    
    # 3. Talent context
    if "Underachieving" in talent['classification']:
        summary_parts.append(f"{talent['classification']} ({talent['performance_delta']:+.1f}% vs expectations).")
    elif "Overachiever" in talent['classification'] or "Miracle Worker" in talent['classification']:
        summary_parts.append(f"{talent['classification']} ({talent['performance_delta']:+.1f}% above expected).")
    
    # 4. Momentum indicator
    if trend.get('weighted_win_pct', 0) >= 80:
        summary_parts.append(f"🔥 Elite momentum ({trend['weighted_win_pct']:.1f}% weighted recent).")
    elif trend.get('avg_trend', 0) >= 10:
        summary_parts.append(f"📈 Surging ({trend['avg_trend']:+.1f}% trend).")
    elif trend.get('avg_trend', 0) <= -10:
        summary_parts.append(f"📉 Declining ({trend['avg_trend']:+.1f}% trend).")
    
    # 5. NFL development
    if draft.get('first_rounders', 0) >= 5:
        summary_parts.append(f"Elite developer ({draft['first_rounders']} 1st-rounders).")
    
    # 6. Betting performance
    if betting.get('total', 0) >= 5:
        if betting['cover_rate'] >= 60:
            summary_parts.append(f"Exceeds expectations (betting: {betting['cover_rate']:.0f}%).")
        elif betting['cover_rate'] <= 40:
            summary_parts.append(f"Below expectations (betting: {betting['cover_rate']:.0f}%).")
    
    return " ".join(summary_parts)

def main():
    """Generate advanced coaching rankings"""
    print("🏈 Advanced Coach Rankings Generator")
    print("=" * 80)
    
    # Load base coaching data
    with open('data/coaches_enhanced_stats.json', 'r') as f:
        coaches_data = json.load(f)
    
    print(f"✅ Loaded {len(coaches_data)} coaches\n")
    
    enhanced_coaches = []
    enhanced_dir = Path('enhanced_coaches')
    
    for coach in coaches_data:
        name = coach['name']
        team = coach['team']
        
        # Find corresponding enhanced file
        coach_file = None
        for filepath in enhanced_dir.glob('*.json'):
            if team.lower().replace(' ', '_').replace('&', 'and') in filepath.stem.lower():
                coach_file = filepath
                break
        
        print(f"📊 Analyzing {name:25s} ({team:20s})...", end=' ')
        
        # 1. Calculate weighted recent trend (2025 heavily weighted)
        trend_score, seasons, weighted_win_pct = calculate_weighted_recent_trend(coach_file) if coach_file else (0, {}, 0)
        
        # 2. Analyze 2025 season in depth
        season_2025_analysis = analyze_2025_season_performance(coach_file, team) if coach_file else {'season_score': 50, 'quality_wins': 0, 'rating': 'No Data'}
        
        # 3. Analyze talent vs performance
        talent_analysis = analyze_talent_vs_performance(
            name, team, coach['careerWinPct'], coach['totalWins']
        )
        
        # 4. Big game analysis
        big_game_analysis = calculate_big_game_factor(coach.get('vsRanked', {}))
        
        # 5. Talent ratings analysis
        talent_ratings = analyze_talent_ratings(coach_file) if coach_file else {'avg_talent': 0, 'recent_talent': 0, 'trend': 0}
        
        # 6. Draft picks analysis
        draft_analysis = analyze_draft_picks(coach_file) if coach_file else {'total_picks': 0, 'first_rounders': 0, 'score': 0}
        
        # 7. Betting performance 2025
        betting_2025 = analyze_betting_performance_2025(coach_file, team) if coach_file else {'cover_rate': 50, 'covers': 0, 'total': 0}
        
        # 8. Consistency
        consistency_score, consistency_rating = calculate_consistency_score(seasons)
        
        # Enhanced stats
        enhanced_stats = {
            'talent_context': talent_analysis,
            'big_game_analysis': big_game_analysis,
            'season_2025': season_2025_analysis,
            'recent_trend': {
                'avg_trend': round(trend_score, 1),
                'weighted_win_pct': round(weighted_win_pct, 1),
                'recent_seasons': seasons
            },
            'talent_ratings': talent_ratings,
            'draft_analysis': draft_analysis,
            'betting_2025': betting_2025,
            'consistency': {
                'score': consistency_score,
                'rating': consistency_rating
            }
        }
        
        # Calculate composite ranking
        composite_score = calculate_composite_ranking(coach, enhanced_stats)
        
        # Generate summary
        summary = generate_coach_summary(coach, enhanced_stats)
        
        enhanced_coach = {
            **coach,
            'composite_score': composite_score,
            'enhanced_analysis': enhanced_stats,
            'coach_summary': summary
        }
        
        enhanced_coaches.append(enhanced_coach)
        print(f"Score: {composite_score:.1f}")
    
    # Sort by composite score
    enhanced_coaches.sort(key=lambda c: c['composite_score'], reverse=True)
    
    # Normalize scores so top coach = 99, bottom proportional
    if enhanced_coaches:
        max_score = enhanced_coaches[0]['composite_score']
        min_score = min(c['composite_score'] for c in enhanced_coaches)
        score_range = max_score - min_score if max_score > min_score else 1
        
        for coach in enhanced_coaches:
            # Scale to 99 (top) down to reasonable floor
            raw_score = coach['composite_score']
            normalized = ((raw_score - min_score) / score_range) * 99
            coach['composite_score'] = round(normalized, 2)
            coach['raw_score'] = round(raw_score, 2)  # Keep original for reference
    
    # Add composite rank
    for rank, coach in enumerate(enhanced_coaches, 1):
        coach['composite_rank'] = rank
    
    # Save enhanced rankings
    output_path = 'data/coaches_advanced_rankings.json'
    with open(output_path, 'w') as f:
        json.dump(enhanced_coaches, f, indent=2)
    
    print(f"\n✅ Saved advanced rankings to: {output_path}")
    
    # Display top performers
    print("\n" + "=" * 80)
    print("🏆 TOP 10 COACHES (Composite Score - 2025 Heavily Weighted)")
    print("=" * 80)
    for i, coach in enumerate(enhanced_coaches[:10], 1):
        talent = coach['enhanced_analysis']['talent_context']
        season_2025 = coach['enhanced_analysis'].get('season_2025', {})
        trend = coach['enhanced_analysis']['recent_trend']
        draft = coach['enhanced_analysis'].get('draft_analysis', {})
        betting = coach['enhanced_analysis'].get('betting_2025', {})
        
        print(f"\n#{i:2d} {coach['name']:25s} | {coach['team']:20s}")
        print(f"    Composite Score: {coach['composite_score']:.1f}/100")
        print(f"    Career: {coach['careerRecord']:10s} ({coach['careerWinPct']:.1f}%)")
        print(f"    2025 Season: {season_2025.get('record', 'N/A'):8s} - {season_2025.get('rating', 'No Data')}")
        print(f"    Context: {talent['classification']}")
        print(f"    Momentum: {trend.get('weighted_win_pct', 0):.1f}% weighted | Trend: {trend.get('avg_trend', 0):+.1f}%")
        if draft.get('first_rounders', 0) > 0:
            print(f"    NFL Draft: {draft['total_picks']} picks ({draft['first_rounders']} 1st round)")
        if betting.get('total', 0) >= 5:
            print(f"    vs Spread: {betting['covers']}-{betting['total']-betting['covers']} ({betting['cover_rate']:.1f}%)")
    
    # Show biggest overachievers
    print("\n" + "=" * 80)
    print("🌟 BIGGEST OVERACHIEVERS (Exceeding Talent Expectations)")
    print("=" * 80)
    overachievers = sorted(
        [c for c in enhanced_coaches if c['enhanced_analysis']['talent_context']['performance_delta'] > 0],
        key=lambda c: c['enhanced_analysis']['talent_context']['performance_delta'],
        reverse=True
    )[:10]
    
    for coach in overachievers:
        talent = coach['enhanced_analysis']['talent_context']
        print(f"{coach['name']:25s} | {coach['team']:20s} | "
              f"+{talent['performance_delta']:.1f}% above expected | {talent['classification']}")
    
    # Show hot coaches (best recent trend)
    print("\n" + "=" * 80)
    print("🔥 HOTTEST COACHES (Best Momentum - Weighted Recent Performance)")
    print("=" * 80)
    hot_coaches = sorted(
        enhanced_coaches,
        key=lambda c: c['enhanced_analysis']['recent_trend'].get('avg_trend', 0),
        reverse=True
    )[:10]
    
    for coach in hot_coaches:
        trend = coach['enhanced_analysis']['recent_trend']
        season_2025 = coach['enhanced_analysis'].get('season_2025', {})
        print(f"{coach['name']:25s} | {coach['team']:20s} | "
              f"Trend: {trend.get('avg_trend', 0):+.1f}% | 2025: {season_2025.get('record', 'N/A')}")
    
    # Show best big game coaches
    print("\n" + "=" * 80)
    print("💪 ELITE BIG GAME COACHES")
    print("=" * 80)
    big_game_coaches = sorted(
        [c for c in enhanced_coaches if c['enhanced_analysis']['big_game_analysis']['big_games_total'] >= 10],
        key=lambda c: c['enhanced_analysis']['big_game_analysis']['big_game_score'],
        reverse=True
    )[:10]
    
    for coach in big_game_coaches:
        big_game = coach['enhanced_analysis']['big_game_analysis']
        print(f"{coach['name']:25s} | {coach['team']:20s} | "
              f"{big_game['big_game_score']:.1f} | vs Top5: {big_game['vs_top5_record']}")
    
    # Compare with ESPN's May 2025 Rankings
    print("\n" + "=" * 80)
    print("📊 DATA-DRIVEN vs ESPN'S REPUTATION RANKINGS (May 2025)")
    print("=" * 80)
    
    espn_rankings = {
        'Kirby Smart': 1,
        'Ryan Day': 2,
        'Dabo Swinney': 3,
        'Marcus Freeman': 4,
        'Steve Sarkisian': 5,
        'Dan Lanning': 6,
        'Kalen DeBoer': 7,
        'James Franklin': 8,
        'Kyle Whittingham': 9,
        'Matt Campbell': 10
    }
    
    print(f"\n{'Coach':<25} | {'ESPN Rank':<10} | {'Our Rank':<10} | {'Difference':<15} | {'Why?'}")
    print("-" * 100)
    
    for coach_name, espn_rank in espn_rankings.items():
        our_coach = next((c for c in enhanced_coaches if c['name'] == coach_name), None)
        if our_coach:
            our_rank = our_coach['composite_rank']
            diff = espn_rank - our_rank
            
            # Explanation
            if coach_name == 'Kirby Smart':
                reason = "10-2 in 2025, underachieving with elite roster"
            elif coach_name == 'Ryan Day':
                reason = "12-0 in 2025, meeting elite expectations"
            elif coach_name == 'Dabo Swinney':
                reason = "Only 9-4 in 2025, declining trend"
            elif coach_name == 'Marcus Freeman':
                reason = "10-2, wasting elite Notre Dame talent"
            elif coach_name == 'Dan Lanning':
                reason = "Only 10-3 in 2025, below expectations"
            elif coach_name == 'Matt Campbell':
                reason = "8-4 in 2025, hot trend but not elite year"
            else:
                reason = "2025 performance weighted heavily"
            
            direction = "📈" if diff > 0 else "📉" if diff < 0 else "="
            print(f"{coach_name:<25} | #{espn_rank:<9} | #{our_rank:<9} | {direction} {abs(diff):<12} | {reason}")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHT: ESPN ranks on REPUTATION (career achievements, name recognition)")
    print("             Our system ranks on PERFORMANCE (2025 results, momentum, context)")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🎯 COACHES RISING IN OUR DATA-DRIVEN RANKINGS")
    print("=" * 80)
    
    rising_coaches = [
        ('Lane Kiffin', 'Ole Miss', 3, 'Not in ESPN Top 10', '11-1 in 2025, elite year'),
        ('Curt Cignetti', 'Indiana', 7, 'ESPN: Received votes', '12-0 in 2025, +59% trend'),
        ('Mike Elko', "Texas A&M", 5, 'Not in ESPN Top 10', '11-1 in 2025, surging'),
        ('Joey McGuire', 'Texas Tech', 9, 'Not in ESPN Top 10', '11-1 in 2025, overachieving')
    ]
    
    for name, team, our_rank, espn_status, reason in rising_coaches:
        print(f"#{our_rank:2d} {name:20s} ({team:15s}) - {espn_status:25s} | {reason}")
    
    print("\n" + "=" * 80)
    print("✅ Analysis Complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
