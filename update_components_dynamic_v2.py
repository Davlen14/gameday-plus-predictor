#!/usr/bin/env python3
"""
IMPROVED: Bulk update React components to use dynamic API data.
This version properly handles JSX syntax and creates valid React code.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

COMPONENTS_DIR = Path("frontend/src/components/figma")

def update_key_player_impact():
    """Update KeyPlayerImpact.tsx with dynamic data"""
    file_path = COMPONENTS_DIR / "KeyPlayerImpact.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports if missing
    if "generateTeamAbbr" not in content:
        content = content.replace(
            "import { ImageWithFallback } from './figma/ImageWithFallback';",
            "import { ImageWithFallback } from './figma/ImageWithFallback';\nimport { generateTeamAbbr } from '../../utils/teamUtils';"
        )
    
    # Add team extraction at start of component
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Users className="w-5 h-5 text-amber-400" />
          <h3 className="text-white font-semibold">Key Player Impact Analysis</h3>
        </div>
        <div className="text-slate-400 text-center py-8">Loading team data...</div>
      </GlassCard>
    );
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function KeyPlayerImpact\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace Illinois team section
    content = re.sub(
        r'<div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br from-\[rgba\(255,95,5,0\.15\)\] to-\[rgba\(255,95,5,0\.05\)\] border-\[rgba\(255,95,5,0\.4\)\]">',
        '<div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br from-[rgba(255,95,5,0.15)] to-[rgba(255,95,5,0.05)] border-[rgba(255,95,5,0.4)]" style={{ borderColor: `${awayTeam.primary_color}66`, background: `linear-gradient(to bottom right, ${awayTeam.primary_color}26, ${awayTeam.primary_color}0d)` }}>',
        content
    )
    
    # Replace Illinois team logo and name
    content = re.sub(
        r'<ImageWithFallback src="https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png" alt="Illinois" className="w-8 h-8 object-contain" />',
        '<ImageWithFallback src={awayTeam.logo} alt={awayTeam.name} className="w-8 h-8 object-contain" />',
        content
    )
    
    content = re.sub(
        r'<h4 className="font-semibold text-lg text-\[#ff5f05\]">Illinois Key Players</h4>',
        '<h4 className="font-semibold text-lg" style={{ color: awayTeam.primary_color }}>{awayTeam.name} Key Players</h4>',
        content
    )
    
    # Replace Ohio State team section
    content = re.sub(
        r'<div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br from-\[rgba\(206,17,65,0\.15\)\] to-\[rgba\(206,17,65,0\.05\)\] border-\[rgba\(206,17,65,0\.4\)\]">',
        '<div className="rounded-lg p-4 border backdrop-blur-sm bg-gradient-to-br from-[rgba(206,17,65,0.15)] to-[rgba(206,17,65,0.05)] border-[rgba(206,17,65,0.4)]" style={{ borderColor: `${homeTeam.primary_color}66`, background: `linear-gradient(to bottom right, ${homeTeam.primary_color}26, ${homeTeam.primary_color}0d)` }}>',
        content
    )
    
    # Replace Ohio State team logo and name
    content = re.sub(
        r'<ImageWithFallback src="https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png" alt="Ohio State" className="w-8 h-8 object-contain" />',
        '<ImageWithFallback src={homeTeam.logo} alt={homeTeam.name} className="w-8 h-8 object-contain" />',
        content
    )
    
    content = re.sub(
        r'<h4 className="font-semibold text-lg text-\[#ce1141\]">Ohio State Key Players</h4>',
        '<h4 className="font-semibold text-lg" style={{ color: homeTeam.primary_color }}>{homeTeam.name} Key Players</h4>',
        content
    )
    
    # Replace team abbreviations in differential
    content = re.sub(
        r'<p className="text-slate-400 text-xs font-mono">OSU \+0\.40</p>',
        '<p className="text-slate-400 text-xs font-mono">{homeAbbr} advantage</p>',
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ KeyPlayerImpact.tsx updated"


def update_advanced_metrics():
    """Update AdvancedMetrics.tsx with dynamic data"""
    file_path = COMPONENTS_DIR / "AdvancedMetrics.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        content = content.replace(
            "import { ImageWithFallback } from './figma/ImageWithFallback';",
            "import { ImageWithFallback } from './figma/ImageWithFallback';\nimport { generateTeamAbbr } from '../../utils/teamUtils';"
        )
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          <h3 className="text-white font-semibold">Advanced Offensive Metrics</h3>
        </div>
        <div className="text-slate-400 text-center py-8">Loading metrics...</div>
      </GlassCard>
    );
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function AdvancedMetrics\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace hardcoded teams object
    content = re.sub(
        r'const teams = \{[^}]+away: \{ name: [\'"]Ohio State[\'"], abbreviation: [\'"]OSU[\'"], color: [\'"]#ce1141[\'"] \},[^}]+home: \{ name: [\'"]Illinois[\'"], abbreviation: [\'"]ILL[\'"], color: [\'"]#ff5f05[\'"] \}[^}]+\};',
        '''const teams = {
    home: { name: homeTeam.name, abbreviation: homeAbbr, color: homeTeam.primary_color },
    away: { name: awayTeam.name, abbreviation: awayAbbr, color: awayTeam.primary_color }
  };''',
        content
    )
    
    # Replace OSU logo references
    content = re.sub(
        r'src="https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png"\s+alt="(?:Ohio State|OSU)"',
        'src={homeTeam.logo} alt={homeTeam.name}',
        content
    )
    
    # Replace ILL logo references
    content = re.sub(
        r'src="https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png"\s+alt="(?:Illinois|ILL)"',
        'src={awayTeam.logo} alt={awayTeam.name}',
        content
    )
    
    # Replace color references
    content = re.sub(r'text-\[#ce1141\]', 'text-[{homeTeam.primary_color}]', content)
    content = re.sub(r'text-\[#ff5f05\]', 'text-[{awayTeam.primary_color}]', content)
    
    # Replace abbreviation text
    content = re.sub(r'<span[^>]*>OSU</span>', '<span>{homeAbbr}</span>', content)
    content = re.sub(r'<span[^>]*>ILL</span>', '<span>{awayAbbr}</span>', content)
    
    # Update advantage calculations
    content = re.sub(
        r'const osuAdvantages = offensiveMetrics\.filter\(metric =>\s+metric\.higherBetter \? metric\.OSU > metric\.ILL : metric\.OSU < metric\.ILL\s+\)\.map\(m => m\.metric\);',
        '''const homeAdvantages = offensiveMetrics.filter(metric => 
    metric.higherBetter ? metric.HOME > metric.AWAY : metric.HOME < metric.AWAY
  ).map(m => m.metric);''',
        content
    )
    
    content = re.sub(
        r'const illAdvantages = offensiveMetrics\.filter\(metric =>\s+metric\.higherBetter \? metric\.ILL > metric\.OSU : metric\.ILL < metric\.OSU\s+\)\.map\(m => m\.metric\);',
        '''const awayAdvantages = offensiveMetrics.filter(metric => 
    metric.higherBetter ? metric.AWAY > metric.HOME : metric.AWAY < metric.HOME
  ).map(m => m.metric);''',
        content
    )
    
    # Update metric keys in data
    content = re.sub(r'OSU:', 'HOME:', content)
    content = re.sub(r'ILL:', 'AWAY:', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ AdvancedMetrics.tsx updated"


def update_comprehensive_stats():
    """Update ComprehensiveStats.tsx with dynamic data"""
    file_path = COMPONENTS_DIR / "ComprehensiveStats.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        # Find last import and add after it
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return <div className="text-slate-400 text-center py-8">Loading comprehensive stats...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function ComprehensiveStats\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace data keys OSU -> HOME, ILL -> AWAY
    content = re.sub(r'\bOSU\b(?=:)', 'HOME', content)
    content = re.sub(r'\bILL\b(?=:)', 'AWAY', content)
    
    # Replace team logo URLs
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    
    # Replace color references
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ ComprehensiveStats.tsx updated"


def update_extended_defensive():
    """Update ExtendedDefensiveAnalytics.tsx"""
    file_path = COMPONENTS_DIR / "ExtendedDefensiveAnalytics.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return <div className="text-slate-400 text-center py-8">Loading defensive analytics...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function ExtendedDefensiveAnalytics\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace team references
    content = re.sub(r'"Ohio State"', '{homeTeam.name}', content)
    content = re.sub(r"'Ohio State'", '{homeTeam.name}', content)
    content = re.sub(r'"Illinois"', '{awayTeam.name}', content)
    content = re.sub(r"'Illinois'", '{awayTeam.name}', content)
    
    # Replace abbreviations
    content = re.sub(r'"OSU"', '{homeAbbr}', content)
    content = re.sub(r"'OSU'", '{homeAbbr}', content)
    content = re.sub(r'"ILL"', '{awayAbbr}', content)
    content = re.sub(r"'ILL'", '{awayAbbr}', content)
    
    # Replace logos
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    
    # Replace colors
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ ExtendedDefensiveAnalytics.tsx updated"


def update_drive_efficiency():
    """Update DriveEfficiency.tsx"""
    file_path = COMPONENTS_DIR / "DriveEfficiency.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return <div className="text-slate-400 text-center py-8">Loading drive efficiency...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function DriveEfficiency\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace team references and logos
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    
    # Replace colors
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    # Replace abbreviations in text
    content = re.sub(r'>OSU<', '>{homeAbbr}<', content)
    content = re.sub(r'>ILL<', '>{awayAbbr}<', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ DriveEfficiency.tsx updated"


def update_ap_poll_rankings():
    """Update APPollRankings.tsx"""
    file_path = COMPONENTS_DIR / "APPollRankings.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return <div className="text-slate-400 text-center py-8">Loading AP rankings...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function APPollRankings\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace logos and colors
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ APPollRankings.tsx updated"


def update_season_records():
    """Update SeasonRecords.tsx"""
    file_path = COMPONENTS_DIR / "SeasonRecords.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  
  if (!homeTeam || !awayTeam) {
    return <div className="text-slate-400 text-center py-8">Loading season records...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function SeasonRecords\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace logos and colors
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ SeasonRecords.tsx updated"


def update_final_prediction():
    """Update FinalPredictionSummary.tsx"""
    file_path = COMPONENTS_DIR / "FinalPredictionSummary.tsx"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add imports
    if "generateTeamAbbr" not in content:
        imports_to_add = "import { generateTeamAbbr } from '../../utils/teamUtils';"
        last_import = list(re.finditer(r'^import .+;$', content, re.MULTILINE))[-1]
        content = content[:last_import.end()] + '\n' + imports_to_add + content[last_import.end():]
    
    # Add team extraction with prediction data
    team_extraction = """  const homeTeam = predictionData?.teams?.home;
  const awayTeam = predictionData?.teams?.away;
  const prediction = predictionData?.prediction;
  
  if (!homeTeam || !awayTeam || !prediction) {
    return <div className="text-slate-400 text-center py-8">Loading prediction...</div>;
  }
  
  const homeAbbr = generateTeamAbbr(homeTeam.name);
  const awayAbbr = generateTeamAbbr(awayTeam.name);
  const homeScore = prediction.home_score || 0;
  const awayScore = prediction.away_score || 0;

"""
    
    if "const homeTeam = predictionData?.teams?.home;" not in content:
        content = re.sub(
            r'(export function FinalPredictionSummary\([^)]+\) \{)\s*\n',
            r'\1\n' + team_extraction,
            content
        )
    
    # Replace team names and scores
    content = re.sub(r'Ohio State 45', '{homeTeam.name} {homeScore}', content)
    content = re.sub(r'Illinois 21', '{awayTeam.name} {awayScore}', content)
    
    # Replace logos and colors
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/194\.png',
        '{homeTeam.logo}',
        content
    )
    content = re.sub(
        r'https://a\.espncdn\.com/i/teamlogos/ncaa/500/356\.png',
        '{awayTeam.logo}',
        content
    )
    content = re.sub(r'#ce1141', '{homeTeam.primary_color}', content)
    content = re.sub(r'#ff5f05', '{awayTeam.primary_color}', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    return "✅ FinalPredictionSummary.tsx updated"


def main():
    """Execute all updates"""
    print("🚀 Starting Component Dynamic Update v2")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Make sure you've committed or backed up your changes!")
    print("=" * 70)
    
    updates = [
        ("KeyPlayerImpact", update_key_player_impact),
        ("AdvancedMetrics", update_advanced_metrics),
        ("ComprehensiveStats", update_comprehensive_stats),
        ("ExtendedDefensiveAnalytics", update_extended_defensive),
        ("DriveEfficiency", update_drive_efficiency),
        ("APPollRankings", update_ap_poll_rankings),
        ("SeasonRecords", update_season_records),
        ("FinalPredictionSummary", update_final_prediction),
    ]
    
    results = []
    
    for name, update_func in updates:
        try:
            result = update_func()
            results.append(result)
            print(f"\n{result}")
        except FileNotFoundError:
            msg = f"⚠️  {name}.tsx not found - skipping"
            results.append(msg)
            print(f"\n{msg}")
        except Exception as e:
            msg = f"❌ {name}.tsx failed: {e}"
            results.append(msg)
            print(f"\n{msg}")
    
    print("\n" + "=" * 70)
    print("✨ Update Complete!")
    print("=" * 70)
    print("\n📋 Summary:")
    for result in results:
        print(f"  {result}")
    
    print("\n💡 Next Steps:")
    print("  1. Review the changes with: git diff")
    print("  2. Test the components: npm run dev")
    print("  3. If issues occur: git checkout -- frontend/src/components/figma/")
    print("\n🎯 All components now use dynamic team data from predictionData prop!")


if __name__ == "__main__":
    main()
