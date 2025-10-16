#!/usr/bin/env python3
"""
Smart React Component Analysis - Distinguish demo/placeholder data from hardcoded issues
"""

import os
import re
from pathlib import Path

def analyze_component_data_usage():
    """Analyze components to distinguish demo data from hardcoded issues"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma")
    
    if not base_path.exists():
        print(f"❌ Components directory not found: {base_path}")
        return {}
    
    print("🎯 SMART REACT COMPONENT DATA ANALYSIS")
    print("=" * 80)
    print("Distinguishing between demo/placeholder data vs hardcoded issues...")
    
    component_files = list(base_path.glob('*.tsx')) + list(base_path.glob('*.jsx'))
    
    analysis_results = {
        'demo_data_components': [],      # Components with good demo data
        'needs_props_integration': [],   # Components that need API integration
        'fully_dynamic': [],             # Components already using props/API
        'problematic': []                # Components with real hardcoded issues
    }
    
    for file_path in component_files:
        try:
            content = file_path.read_text()
            component_name = file_path.stem
            
            # Check for different patterns
            has_props = bool(re.search(r'(props\.|interface.*Props|type.*Props)', content))
            has_state = bool(re.search(r'(useState|useReducer)', content))
            has_api_calls = bool(re.search(r'(fetch|axios|api\.|/predict)', content))
            has_conditional_rendering = bool(re.search(r'{\s*\w+\s*\?\s*.*\s*:\s*.*}', content))
            
            # Look for demo/placeholder patterns (good)
            demo_patterns = [
                r'// Demo data|// Placeholder|// Example',
                r'const\s+demo\w*|const\s+placeholder\w*|const\s+sample\w*',
                r'defaultValue|initialValue|fallback',
                r'before.*prediction|until.*data|loading.*state'
            ]
            
            has_demo_indicators = any(re.search(pattern, content, re.IGNORECASE) for pattern in demo_patterns)
            
            # Look for problematic hardcoded patterns (bad)
            problematic_patterns = [
                r'return\s*<[^>]*>[^<]*USC[^<]*</[^>]*>',  # Direct USC rendering
                r'const\s+\w+\s*=\s*["\']USC["\']',        # USC as constant
                r'<[^>]*>\s*24-17\s*</[^>]*>',            # Hardcoded scores
                r'Lincoln Riley|Marcus Freeman'             # Hardcoded coaches
            ]
            
            has_problematic = any(re.search(pattern, content, re.IGNORECASE) for pattern in problematic_patterns)
            
            # Look for visual/demo team references (acceptable)
            visual_demo_patterns = [
                r'alt=["\'](Ohio State|Illinois|USC|Notre Dame)["\']',  # Image alt text
                r'className.*team-logo',                                # Logo classes
                r'// Visual example|// UI preview|// Design showcase'   # Comments indicating demo
            ]
            
            has_visual_demo = any(re.search(pattern, content, re.IGNORECASE) for pattern in visual_demo_patterns)
            
            # Categorize component
            component_info = {
                'name': component_name,
                'has_props': has_props,
                'has_state': has_state,
                'has_api_calls': has_api_calls,
                'has_conditional_rendering': has_conditional_rendering,
                'has_demo_indicators': has_demo_indicators,
                'has_visual_demo': has_visual_demo,
                'has_problematic': has_problematic,
                'file_size': len(content),
                'jsx_expressions': len(re.findall(r'{[^}]+}', content))
            }
            
            # Classify component
            if has_api_calls and has_props and has_conditional_rendering:
                analysis_results['fully_dynamic'].append(component_info)
            elif has_problematic:
                analysis_results['problematic'].append(component_info)
            elif has_visual_demo or has_demo_indicators:
                analysis_results['demo_data_components'].append(component_info)
            elif not has_props and not has_api_calls:
                analysis_results['needs_props_integration'].append(component_info)
            else:
                analysis_results['demo_data_components'].append(component_info)  # Default to demo
                
        except Exception as e:
            print(f"⚠️  Error analyzing {file_path.name}: {e}")
    
    return analysis_results

def create_integration_recommendations(analysis_results):
    """Create specific recommendations for each component category"""
    
    print(f"\n📊 COMPONENT CATEGORIZATION RESULTS")
    print("=" * 80)
    
    # Fully Dynamic (Already Good)
    print(f"\n✅ FULLY DYNAMIC COMPONENTS ({len(analysis_results['fully_dynamic'])})")
    print("These components are already properly integrated:")
    for comp in analysis_results['fully_dynamic']:
        print(f"   🎯 {comp['name']} - Props: ✅ API: ✅ Conditional: ✅")
    
    # Demo Data (Keep As-Is)  
    print(f"\n🎨 DEMO/PLACEHOLDER COMPONENTS ({len(analysis_results['demo_data_components'])})")
    print("These components show visual demos before prediction - KEEP THEM:")
    for comp in analysis_results['demo_data_components']:
        status_props = "✅" if comp['has_props'] else "➕"
        status_state = "✅" if comp['has_state'] else "➕"
        print(f"   🎨 {comp['name']} - Props: {status_props} State: {status_state} JSX: {comp['jsx_expressions']}")
    
    # Need Props Integration  
    print(f"\n🔧 NEED PROPS INTEGRATION ({len(analysis_results['needs_props_integration'])})")
    print("These components need to accept props from parent:")
    for comp in analysis_results['needs_props_integration']:
        print(f"   🔧 {comp['name']} - Add props interface and conditional rendering")
    
    # Problematic (Fix Required)
    print(f"\n🚨 PROBLEMATIC COMPONENTS ({len(analysis_results['problematic'])})")
    print("These components have real hardcoded issues to fix:")
    for comp in analysis_results['problematic']:
        print(f"   🚨 {comp['name']} - Remove hardcoded coaches/teams")

def show_ideal_pattern():
    """Show the ideal component pattern for demo + dynamic data"""
    
    print(f"\n🎯 RECOMMENDED COMPONENT PATTERN")
    print("=" * 80)
    
    pattern_example = '''
// ✅ IDEAL PATTERN: Demo data + Dynamic integration

interface ComponentProps {
  predictionData?: PredictionData;  // Optional - undefined before prediction
  isLoading?: boolean;
}

export function MyComponent({ predictionData, isLoading }: ComponentProps) {
  // Demo/placeholder data (KEEP THIS!)
  const demoData = {
    homeTeam: "Ohio State", 
    awayTeam: "Illinois",
    homeScore: 24,
    awayScore: 17
  };
  
  // Use real data if available, otherwise show demo
  const displayData = predictionData || demoData;
  const showDemo = !predictionData && !isLoading;
  
  return (
    <div>
      {showDemo && (
        <div className="demo-badge">Preview Mode</div>
      )}
      
      <TeamDisplay 
        homeTeam={displayData.homeTeam}
        awayTeam={displayData.awayTeam}
      />
      
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <ScoreDisplay 
          homeScore={displayData.homeScore}
          awayScore={displayData.awayScore}
        />
      )}
    </div>
  );
}
    '''
    
    print(pattern_example)

def analyze_specific_components():
    """Look at specific components that were flagged"""
    
    print(f"\n🔍 DETAILED COMPONENT ANALYSIS")
    print("=" * 80)
    
    specific_components = [
        'FieldPositionMetrics.tsx',
        'TeamSelector.tsx', 
        'EPAComparison.tsx',
        'ComponentBreakdown.tsx'
    ]
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma")
    
    for comp_name in specific_components:
        comp_path = base_path / comp_name
        
        if not comp_path.exists():
            print(f"❌ {comp_name} - Not found")
            continue
            
        try:
            content = comp_path.read_text()
            
            # Check for demo vs hardcoded
            team_refs = re.findall(r'\b(Ohio State|Illinois|USC|Notre Dame)\b', content)
            alt_text_refs = re.findall(r'alt=["\']([^"\']*)["\']', content)
            coach_refs = re.findall(r'\b(Lincoln Riley|Marcus Freeman)\b', content)
            
            print(f"\n📄 {comp_name}")
            print(f"   🏈 Team References: {len(set(team_refs))} - {', '.join(set(team_refs))}")
            print(f"   🖼️  Alt Text Usage: {len(alt_text_refs)} (likely demo images)")
            print(f"   👨‍🏫 Coach References: {len(coach_refs)}")
            
            # Determine if it's demo or problematic
            if alt_text_refs and not coach_refs:
                print(f"   ✅ VERDICT: Demo/Visual data - KEEP IT")
            elif coach_refs:
                print(f"   🚨 VERDICT: Hardcoded coaches - NEEDS FIXING") 
            else:
                print(f"   🎨 VERDICT: Visual placeholders - ACCEPTABLE")
                
        except Exception as e:
            print(f"❌ Error analyzing {comp_name}: {e}")

if __name__ == "__main__":
    print("🎯 SMART COMPONENT DATA ANALYSIS")
    print("=" * 80)
    
    # Analyze all components
    results = analyze_component_data_usage()
    
    # Show categorization
    create_integration_recommendations(results)
    
    # Show ideal pattern
    show_ideal_pattern()
    
    # Detailed analysis
    analyze_specific_components()
    
    print(f"\n🎯 FINAL RECOMMENDATION")
    print("=" * 80)
    print("✅ KEEP demo/placeholder data for visual preview")
    print("✅ ADD props interfaces to accept real prediction data") 
    print("✅ USE conditional rendering: demo → loading → real data")
    print("🚨 ONLY fix components with hardcoded coaches/problematic data")
    print("\n💡 Your approach is PERFECT - visual demos + dynamic data!")