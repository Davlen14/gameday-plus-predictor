#!/usr/bin/env python3
"""
React Components Hardcoded Data Detection - Scan figma components for static values
"""

import os
import re
from pathlib import Path

def scan_react_components():
    """Scan React components for hardcoded data patterns"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma")
    
    if not base_path.exists():
        print(f"❌ Components directory not found: {base_path}")
        return {}
    
    # React/JSX hardcoded patterns
    hardcoded_patterns = {
        'team_names': [
            r'\b(USC|Notre Dame|Alabama|Georgia|Ohio State|Michigan)\b',
            r'\b(Trojans|Fighting Irish|Crimson Tide|Bulldogs|Buckeyes|Wolverines)\b',
            r'["\']([A-Z][a-z]+\s+[A-Z][a-z]+)["\']'  # "Team Name" patterns
        ],
        'coach_names': [
            r'\b(Lincoln Riley|Marcus Freeman|Nick Saban|Kirby Smart)\b',
            r'Coach[:\s]*[A-Z][a-z]+\s+[A-Z][a-z]+',
            r'["\']([A-Z][a-z]+\s+[A-Z][a-z]+)["\'].*[Cc]oach'
        ],
        'static_scores': [
            r'\b\d{1,2}-\d{1,2}\b',  # Score patterns like 24-17
            r'Score[:\s]*\d+-\d+',
            r'Final[:\s]*\d+-\d+',
            r'>\d{1,2}</.*>\d{1,2}<'  # JSX score displays
        ],
        'static_stats': [
            r'\b\d+\.\d+\s*(yards|yds|touchdowns|tds|completions)\b',
            r'Passing[:\s]*\d+/\d+',
            r'Rushing[:\s]*\d+\s*yards',
            r'>\d+\.\d+<',  # JSX number displays
            r'>\d+</.*>yards<'
        ],
        'static_percentages': [
            r'\b\d{1,2}\.\d+%',
            r'Win Probability[:\s]*\d+\.\d+%',
            r'Confidence[:\s]*\d+\.\d+%',
            r'>\d{1,2}\.\d+%<'  # JSX percentage displays
        ],
        'hardcoded_predictions': [
            r'Spread[:\s]*[+-]?\d+\.\d+',
            r'Total[:\s]*\d+\.\d+',
            r'Over/Under[:\s]*\d+\.\d+'
        ],
        'static_jsx_content': [
            r'<[^>]*>\s*[A-Z][a-z]+\s+vs\s+[A-Z][a-z]+\s*</[^>]*>',  # Team vs Team
            r'<[^>]*>\s*\d{1,2}-\d{1,2}\s*</[^>]*>',  # Score displays
            r'<[^>]*>\s*Week\s+\d+\s*</[^>]*>'  # Week displays
        ],
        'demo_data': [
            r'const\s+\w+\s*=\s*{[^}]*["\'][A-Z][a-z]+\s+[A-Z][a-z]+["\']',  # Demo objects
            r'useState\([^)]*["\'][A-Z][a-z]+["\'][^)]*\)',  # useState with team names
            r'defaultValue[:\s]*["\'][A-Z][a-z]+["\']'  # Default form values
        ]
    }
    
    # Find all component files
    component_files = []
    for ext in ['*.tsx', '*.jsx', '*.ts', '*.js']:
        component_files.extend(base_path.glob(f'{ext}'))
    
    print("🔍 REACT COMPONENTS HARDCODED DATA SCAN")
    print("=" * 80)
    print(f"📁 Scanning {len(component_files)} React component files...")
    
    findings = {}
    total_issues = 0
    
    for file_path in component_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            file_issues = []
            
            for category, patterns in hardcoded_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        # Get line number
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = content.split('\n')[line_num - 1].strip()
                        
                        # Skip common false positives
                        false_positives = [
                            'import', 'export', 'className', 'style', 'function',
                            'const', 'let', 'var', '//', '/*', '*/', 'console',
                            'tailwind', 'bg-', 'text-', 'px-', 'py-', 'mx-', 'my-'
                        ]
                        
                        if not any(fp in line_content.lower() for fp in false_positives):
                            file_issues.append({
                                'category': category,
                                'pattern': pattern,
                                'match': match.group(),
                                'line': line_num,
                                'line_content': line_content
                            })
            
            if file_issues:
                findings[str(file_path)] = file_issues
                total_issues += len(file_issues)
                
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")
    
    return findings, total_issues, len(component_files)

def check_api_integration():
    """Check if components are set up to receive API data"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma")
    
    print(f"\n🔗 API INTEGRATION CHECK")
    print("=" * 80)
    
    integration_patterns = {
        'props_usage': r'(props\.|{[^}]*}.*props)',
        'api_calls': r'(fetch|axios|api\.|useEffect)',
        'state_management': r'(useState|useContext|useSelector)',
        'dynamic_content': r'({[^}]*\w+[^}]*})',  # JSX expressions
        'conditional_rendering': r'({\s*\w+\s*\?\s*.*\s*:\s*.*})',
        'map_functions': r'(\.map\(|\.filter\(|\.reduce\()'
    }
    
    component_files = list(base_path.glob('*.tsx')) + list(base_path.glob('*.jsx'))
    
    for file_path in component_files[:10]:  # Check first 10 components
        try:
            content = file_path.read_text()
            component_name = file_path.stem
            
            print(f"\n📄 {component_name}")
            
            for pattern_name, pattern in integration_patterns.items():
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                status = "✅" if matches > 0 else "❌"
                print(f"   {status} {pattern_name.replace('_', ' ').title()}: {matches}")
            
            # Check for hardcoded JSX content
            jsx_content = re.findall(r'<[^>]*>([^<]+)</[^>]*>', content)
            static_content = [c for c in jsx_content if re.match(r'^[A-Z][a-z]+.*vs.*[A-Z][a-z]+$', c.strip())]
            
            if static_content:
                print(f"   ⚠️  Static JSX Content: {len(static_content)} found")
                for static in static_content[:3]:  # Show first 3
                    print(f"      '{static.strip()}'")
                    
        except Exception as e:
            print(f"❌ Error reading {component_name}: {e}")

def analyze_component_structure():
    """Analyze overall component structure and patterns"""
    
    base_path = Path("/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma")
    
    print(f"\n📊 COMPONENT STRUCTURE ANALYSIS")
    print("=" * 80)
    
    component_files = list(base_path.glob('*.tsx')) + list(base_path.glob('*.jsx'))
    
    structure_stats = {
        'total_files': len(component_files),
        'uses_props': 0,
        'uses_state': 0,
        'uses_effects': 0,
        'has_api_calls': 0,
        'has_hardcoded_jsx': 0
    }
    
    for file_path in component_files:
        try:
            content = file_path.read_text()
            
            if re.search(r'props\.|interface.*Props|type.*Props', content):
                structure_stats['uses_props'] += 1
                
            if re.search(r'useState|useReducer', content):
                structure_stats['uses_state'] += 1
                
            if re.search(r'useEffect|useLayoutEffect', content):
                structure_stats['uses_effects'] += 1
                
            if re.search(r'fetch|axios|api\.|/predict', content):
                structure_stats['has_api_calls'] += 1
                
            # Check for potentially hardcoded JSX
            jsx_matches = re.findall(r'<[^>]*>([^<{]+)</[^>]*>', content)
            for match in jsx_matches:
                if any(team in match for team in ['USC', 'Notre Dame', 'Alabama', 'Georgia']) or \
                   re.match(r'^\d{1,2}-\d{1,2}$', match.strip()):
                    structure_stats['has_hardcoded_jsx'] += 1
                    break
                    
        except Exception as e:
            print(f"Error analyzing {file_path.name}: {e}")
    
    print(f"📊 Structure Statistics:")
    print(f"   📄 Total Components: {structure_stats['total_files']}")
    print(f"   📦 Uses Props: {structure_stats['uses_props']}")
    print(f"   🔄 Uses State: {structure_stats['uses_state']}")
    print(f"   ⚡ Uses Effects: {structure_stats['uses_effects']}")
    print(f"   🌐 Has API Calls: {structure_stats['has_api_calls']}")
    print(f"   ⚠️  Hardcoded JSX: {structure_stats['has_hardcoded_jsx']}")
    
    # Calculate readiness percentage
    readiness_score = (
        (structure_stats['uses_props'] / structure_stats['total_files'] * 30) +
        (structure_stats['uses_state'] / structure_stats['total_files'] * 20) +
        (structure_stats['has_api_calls'] / structure_stats['total_files'] * 30) +
        ((structure_stats['total_files'] - structure_stats['has_hardcoded_jsx']) / structure_stats['total_files'] * 20)
    )
    
    print(f"\n🎯 Component Readiness Score: {readiness_score:.1f}%")
    
    return structure_stats

if __name__ == "__main__":
    print("🎯 REACT COMPONENTS HARDCODED DATA ANALYSIS")
    print("=" * 80)
    
    # Scan for hardcoded data
    findings, total_issues, total_files = scan_react_components()
    
    # Report findings
    if findings:
        print(f"\n🚨 FOUND {total_issues} POTENTIAL HARDCODED ISSUES IN {len(findings)} COMPONENTS")
        print("=" * 80)
        
        for file_path, issues in list(findings.items())[:5]:  # Show first 5 files
            rel_path = Path(file_path).name
            print(f"\n📄 {rel_path} ({len(issues)} issues)")
            print("-" * 60)
            
            by_category = {}
            for issue in issues:
                cat = issue['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(issue)
            
            for category, cat_issues in by_category.items():
                print(f"\n🎯 {category.upper().replace('_', ' ')} ({len(cat_issues)} found):")
                for issue in cat_issues[:3]:  # Show first 3 of each category
                    print(f"   Line {issue['line']:3d}: {issue['match']}")
                    print(f"            {issue['line_content'][:80]}{'...' if len(issue['line_content']) > 80 else ''}")
        
        if len(findings) > 5:
            print(f"\n... and {len(findings) - 5} more files with issues")
            
    else:
        print("\n✅ NO HARDCODED DATA PATTERNS FOUND IN REACT COMPONENTS!")
        print("All components appear ready for dynamic data.")
    
    # Check API integration readiness
    check_api_integration()
    
    # Analyze component structure
    structure_stats = analyze_component_structure()
    
    print(f"\n🎯 SUMMARY")
    print("=" * 80)
    
    if findings:
        print(f"🚨 Found potential hardcoded issues in {len(findings)}/{total_files} components")
        print("   Review components for static team names, scores, or stats")
    else:
        print("✅ No obvious hardcoded patterns in React components")
        
    print(f"📊 API Integration: {structure_stats['has_api_calls']}/{total_files} components")
    print(f"📦 Props Usage: {structure_stats['uses_props']}/{total_files} components")
    
    print("\n💡 RECOMMENDATIONS:")
    print("   1. Ensure components receive data via props from API")
    print("   2. Replace any hardcoded team names with dynamic props")
    print("   3. Use conditional rendering for loading states")
    print("   4. Test components with different team data")